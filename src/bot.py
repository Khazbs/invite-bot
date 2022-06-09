from discord.ext import commands
import discord
import dateparser
import os

import db

# intents = discord.Intents(guilds=True, members=True, messages=True)
# bot = commands.Bot(command_prefix='!', intents=intents)
bot = commands.Bot(command_prefix='!')


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
async def create(ctx, code=None):
	if not code:
		code = generate_code()
	invite = db.Invite.get_or_none(code=code)
	if invite:
		await ctx.send(f'{invite} already exists')
		return
	invite = db.Invite.create(code=code, guild=ctx.guild.id)
	await ctx.send(f'{invite} now created')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def activate(ctx, code):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	if invite.is_active:
		await ctx.send(f'{invite} already active')
		return
	invite.is_active = True
	invite.save()
	await ctx.send(f'{invite} now activated')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def deactivate(ctx, code):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	if not invite.is_active:
		await ctx.send(f'{code} already inactive')
		return
	invite.is_active = False
	invite.save()
	await ctx.send(f'{invite} now deactivated')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def valid_from(ctx, code, *dt_strings):
	dt_string = ' '.join(dt_strings)
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	dt = parse_from_dt(dt_string)
	if not dt:
		await ctx.send(f'{dt_string} datetime not recognized')
		return
	invite.valid_from = dt.timestamp() * 1000
	invite.save()
	await ctx.send(f'{invite} now valid from {dt}')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def valid_from_anytime(ctx, code):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	invite.valid_from = None
	invite.save()
	await ctx.send(f'{invite} now valid from anytime')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def valid_to(ctx, code, *dt_strings):
	dt_string = ' '.join(dt_strings)
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	dt = parse_to_dt(dt_string)
	if not dt:
		await ctx.send(f'{dt_string} datetime not recognized')
		return
	invite.valid_to = dt.timestamp() * 1000
	invite.save()
	await ctx.send(f'{invite} now valid to {dt}')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def valid_to_anytime(ctx, code):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	invite.valid_from = None
	invite.save()
	await ctx.send(f'{invite} now valid from anytime')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def limit_uses(ctx, code, n_string):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	n = parse_n(n_string)
	if not n:
		await ctx.send(f'{n_string} is not a decimal natural number')
		return
	invite.max_uses = n
	invite.save()
	await ctx.send(f'{invite} now limited to {n} uses')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def unlimit_uses(ctx, code):
	invite = db.Invite.get_or_none(code=code, guild=ctx.guild.id)
	if not invite:
		await ctx.send(f'{code} not found')
		return
	invite.max_uses = None
	invite.save()
	await ctx.send(f'{invite} now unlimited in uses')


@bot.command()
@commands.guild_only()
@commands.check(is_from_command_channel)
async def list_all(ctx):
	invites = db.Invite.select().where(
		db.Invite.guild == ctx.guild.id
	)
	if not invites:
		await ctx.send('No invites yet')
		return
	await ctx.send(f'{", ".join(invite.code for invite in invites)}')


@bot.event
async def on_command_error(ctx, error):
	await ctx.send(f'Uh-oh, {error}')


def run():
	db.init()
	bot.run(os.environ['TOKEN'])


if __name__ == '__main__':
	run()
