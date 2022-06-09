from discord.ext import commands
import discord
import dateparser
import os

import db
import strings as s

# intents = discord.Intents(guilds=True, members=True, messages=True)
# bot = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!', help_command=None)


class UserError(commands.CommandError):
	pass


def is_from_command_channel(ctx):
	return ctx.message.channel.name == os.environ['COMMAND_CHANNEL']


def generate_code():
	return 'TODO'


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


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def select(ctx, code=None):
	if not code:
		raise UserError(s.error_code_missing())
	invite = db.Invite.get_or_none(guild=ctx.guild.id, code=code)
	if not invite:
		raise UserError(s.error_not_found(code))
	existing_invites = list(db.Invite.select().where(db.Invite.guild == ctx.guild.id))
	for existing_invite in existing_invites:
		existing_invite.is_selected = existing_invite == invite
	db.Invite.bulk_update(existing_invites, fields=(
		db.Invite.is_selected,
	))
	await ctx.send(s.success_select(invite.code))


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def create(ctx, code=None):
	if not code:
		code = generate_code()
	invite = db.Invite.get_or_none(guild=ctx.guild.id, code=code)
	if invite:
		raise UserError(s.error_exists(invite.code))
	existing_invites = list(db.Invite.select().where(db.Invite.guild == ctx.guild.id))
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
	invite.uses = n
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
	existing_invites = list(db.Invite.select().where(db.Invite.guild == ctx.guild.id))
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
	else:
		await ctx.send(s.error_server())
		raise error


def run():
	db.init()
	bot.run(os.environ['TOKEN'])


if __name__ == '__main__':
	run()
