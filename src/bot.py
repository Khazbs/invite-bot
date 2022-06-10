from discord.ext import commands
from time import time
import discord
import dateparser
import os

import db
import strings as s

bot = commands.Bot(command_prefix='!', help_command=None)


class UserError(commands.CommandError):
	pass


def is_from_command_channel(ctx):
	channel = ctx.message.channel
	return (channel.name == os.environ['COMMAND_CHANNEL']
		and channel.overwrites[ctx.guild.default_role].read_messages is False)


def generate_code():
	return 'GENERATION NOT YET IMPLEMENTED'


async def give_role(member_id, guild_id):
	guild = await bot.fetch_guild(guild_id)
	member = await guild.fetch_member(member_id)
	for role in member.roles:
		if role.name == os.environ['ROLE']:
			return False
	await member.add_roles(*(
		role for role in guild.roles
		if role.name == os.environ['ROLE']
	))
	return True


def parse_from_dt(dt_string):
	return dateparser.parse(dt_string, settings={
		'PREFER_DAY_OF_MONTH': 'first'
	})


def parse_to_dt(dt_string):
	return dateparser.parse(dt_string, settings={
		'PREFER_DAY_OF_MONTH': 'last'
	})


def parse_n(n_string):
	try:
		n = int(n_string, 10)
	except ValueError:
		return None
	if n < 1:
		return None
	return n


async def create_channels(guild):
	command_ch = await guild.create_text_channel(os.environ['COMMAND_CHANNEL'],
		overwrites={
			bot.user: discord.PermissionOverwrite(
				read_messages=True,
				send_messages=True
			),
			guild.default_role: discord.PermissionOverwrite(
				read_messages=False
			),
		}
	)
	invite_ch = await guild.create_text_channel(os.environ['INVITE_CHANNEL'],
		overwrites={
			bot.user: discord.PermissionOverwrite(
				send_messages=True,
			),
			guild.default_role: discord.PermissionOverwrite(
				send_messages=False
			),
		}
	)
	await command_ch.send(s.invite_setup())
	message = await invite_ch.send(s.invite_guild())
	await message.add_reaction('🤙')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def select(ctx, *code_strings):
	if not code_strings:
		raise UserError(s.error_code_missing())
	code = ' '.join(code_strings)
	invite = db.Invite.get_or_none(guild=ctx.guild.id, code=code)
	if not invite:
		raise UserError(s.error_not_found(code))
	existing_invites = list(db.Invite
		.select()
		.where(db.Invite.guild == ctx.guild.id)
	)
	if existing_invites:
		for existing_invite in existing_invites:
			existing_invite.is_selected = existing_invite == invite
		db.Invite.bulk_update(existing_invites, fields=(
			db.Invite.is_selected,
		))
	await ctx.send(s.success_select(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def create(ctx, *code_strings):
	if code_strings:
		code = ' '.join(code_strings)
	else:
		code = generate_code()
	invite = db.Invite.get_or_none(guild=ctx.guild.id, code=code)
	if invite:
		raise UserError(s.error_exists(invite.code))
	existing_invites = list(db.Invite
		.select()
		.where(db.Invite.guild == ctx.guild.id)
	)
	if existing_invites:
		for existing_invite in existing_invites:
			existing_invite.is_selected = False
		db.Invite.bulk_update(existing_invites, fields=(
			db.Invite.is_selected,
		))
	invite = db.Invite.create(code=code, guild=ctx.guild.id)
	await ctx.send(s.success_create(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def activate(ctx):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	if invite.is_active:
		raise UserError(s.error_active(invite.code))
	invite.is_active = True
	invite.save()
	await ctx.send(s.success_activate(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def deactivate(ctx):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	if not invite.is_active:
		raise UserError(s.error_inactive(invite.code))
	invite.is_active = False
	invite.save()
	await ctx.send(s.success_deactivate(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def begin(ctx, *dt_strings):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	dt_string = ' '.join(dt_strings)
	dt = parse_from_dt(dt_string)
	if not dt:
		raise UserError(s.error_begin_datetime(dt_string))
	invite.begins_ts = dt.timestamp() * 1000
	invite.save()
	await ctx.send(s.success_begin(invite.code, dt))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def begin_anytime(ctx):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	invite.begins_ts = None
	invite.save()
	await ctx.send(s.success_begin_anytime(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def expire(ctx, *dt_strings):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	dt_string = ' '.join(dt_strings)
	dt = parse_to_dt(dt_string)
	if not dt:
		raise UserError(s.error_expire_datetime(dt_string))
	invite.expires_ts = dt.timestamp() * 1000
	invite.save()
	await ctx.send(s.success_expire(invite.code, dt))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def never_expire(ctx):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	invite.expires_ts = None
	invite.save()
	await ctx.send(s.success_never_expire(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def limit(ctx, *n_strings):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	n_string = ''.join(n_strings)
	n = parse_n(n_string)
	if not n:
		raise UserError(s.error_limit_number(n_string))
	invite.max_uses = n
	invite.save()
	await ctx.send(s.success_limit(invite.code, n))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def unlimit(ctx):
	invite = db.Invite.get_or_none(guild=ctx.guild.id, is_selected=True)
	if not invite:
		raise UserError(s.error_not_selected())
	invite.max_uses = None
	invite.save()
	await ctx.send(s.success_unlimit(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def list_all(ctx):
	existing_invites = list(db.Invite
		.select()
		.where(db.Invite.guild == ctx.guild.id)
	)
	if not existing_invites:
		raise UserError(s.error_no_invites())
	await ctx.send(', '.join(
		existing_invite.code for existing_invite in existing_invites
	))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def help(ctx):
	await ctx.send(s.help())


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		msg = str(error)
		command = msg[msg.find('"') + 1:msg.rfind('"')]
		await ctx.send(s.error_unknown_command(command))
	elif isinstance(error, UserError):
		await ctx.send(str(error))
	elif isinstance(error, commands.errors.CheckFailure):
		raise error
	else:
		await ctx.send(s.error_server())
		raise error


@bot.event
async def on_raw_reaction_add(raw_reaction):
	channel = await bot.fetch_channel(raw_reaction.channel_id)
	if not isinstance(channel, discord.abc.GuildChannel):
		return
	if channel.name == os.environ['INVITE_CHANNEL']:
		member = raw_reaction.member
		if member.bot:
			return
		guild = await bot.fetch_guild(raw_reaction.guild_id)
		candidate, created = db.Candidate.get_or_create(user=member.id)
		candidate.guild = guild.id
		candidate.save()
		await member.send(s.invite_dm(guild.name))


@bot.event
async def on_message(message):
	if message.author.bot:
		return
	await bot.process_commands(message)
	if isinstance(message.channel, discord.channel.DMChannel):
		candidate = db.Candidate.get_or_none(user=message.author.id)
		if not (candidate and candidate.guild):
			return
		invite = db.Invite.get_or_none(
			guild=candidate.guild,
			code=message.content
		)
		if not (invite
				and invite.is_active
				and (not invite.begins_ts
					or invite.begins_ts <= time() * 1000)
				and (not invite.expires_ts
					or invite.expires_ts > time() * 1000)
				and (not invite.max_uses
					or invite.max_uses > len(invite.uses))):
			await message.author.send(s.invite_invalid())
			return
		if db.InviteUse.get_or_none(invite=invite.id, user=candidate.user):
			await message.author.send(s.invite_invalid())
			return
		if not await give_role(candidate.user, candidate.guild):
			await message.author.send(s.invite_invalid())
			return
		db.InviteUse.create(
			invite=invite.id,
			user=candidate.user,
			used_ts=time() * 1000
		)
		candidate.guild = None
		candidate.save()
		await message.author.send(s.invite_valid())


@bot.event
async def on_guild_join(guild):
	await create_channels(guild)


def run():
	db.init()
	bot.run(os.environ['TOKEN'])


if __name__ == '__main__':
	run()
