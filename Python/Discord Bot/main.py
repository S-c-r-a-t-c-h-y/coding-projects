import discord
from discord.ext import commands
from random import choice


bot = commands.Bot(command_prefix='s!', description='Lazy dev doing shit...')

@bot.command()
@commands.guild_only()
async def serverinfo(ctx):
	server = ctx.guild
	nb_text_channels = len(server.text_channels)
	nb_voice_channels = len(server.voice_channels)
	desc = server.description
	nb_members = server.member_count
	name = server.name
	desc = f"\nThe description is {desc}." if desc else ''
	await ctx.send(f'The **{name}** server has currently *{nb_members}* members.\n\
	It has a total of {nb_text_channels} text channels and {nb_voice_channels} voice channels.{desc}')


@bot.command()
async def random(ctx, *args):
	await ctx.send(choice(args))

""" ---------- moderations commands ---------- """

@bot.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def ban(ctx, users: commands.Greedy[discord.User], *, reason = "No reason specified"):
	for user in users:
		try:
			await ctx.guild.ban(user, reason=reason)
			await ctx.send(f'{user} has been banned for the reason : *{reason}*.')
		except:
			await ctx.send('I could not find the user you were searching for ...')


@bot.command()
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user, *, reason = "No reason specified"):
	user_name, user_id = user.split('#')
	banned_users = await ctx.guild.bans()
	for banned_user in banned_users:
		if banned_user.user.name == user_name and banned_user.user.discriminator == user_id:
			await ctx.guild.unban(banned_user.user, reason=reason)
			await ctx.send(f'{user} has been unbanned for the reason : *{reason}*.')
			return
	await ctx.send('I could not find the user you were searching for ...')


@bot.command()
@commands.guild_only()
@commands.has_permissions(kick_members=True)
async def kick(ctx, users: commands.Greedy[discord.User], *, reason = "No reason specified"):
	for user in users:
		try:
			await ctx.guild.kick(user, reason=reason)
			await ctx.send(f'{user} has been kicked for the reason : *{reason}*.')
		except:
			await ctx.send('I could not find the user you were searching for ...')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nb: int):
	messages = await ctx.channel.history(limit=nb+1).flatten()
	for mess in messages:
		await mess.delete()
	await ctx.send(f'{nb} messages has been deleted.')


# ----------------------- function used to mute and unmute people, do not pay attention ------------------
async def get_muted_role(ctx):

		async def create_muted_role(ctx):
			muted_role = await ctx.guild.create_role(name='muted', permissions=discord.Permissons(
													send_messages=False,
													speak=False),
													reason="Created a new muted role to mute people with the 'mute' command")
			for channel in ctx.guild.channels:
				await channel.set_permissions(muted_role, send_messages=False, speak=False)
			return muted_role

		for role in ctx.guild.roles:
			if role.name == "muted":
				return role

		return await create_muted_role(ctx)

# --------------------------------------------------------------------------------------------------------


@bot.command()
@commands.has_permissions(deafen_members=True)
async def mute(ctx, member: discord.Member, *, reason = "No reason specified"):
	muted_role = await get_muted_role(ctx)
	await member.add_roles(muted_role, reason=reason)
	await ctx.send(f"{member.mention} got muted !")


@bot.command()
@commands.has_permissions(deafen_members=True)
async def unmute(ctx, member: discord.Member, *, reason = "No reason specified"):
	muted_role = await get_muted_role(ctx)
	await member.remove_roles(muted_role, reason=reason)
	await ctx.send(f"{member.mention} got unmuted !")

@bot.command()
async def id(ctx, *, member: discord.Member):
	await ctx.send(f'{member.mention}: id = {member.id}')

@bot.command()
async def modify(ctx, *args):
	if ctx.channel.id != 850806578125864981:
		pass
	if True:
		sets = [] # stocking every sets found
		subset = [] #I call a 'set' a pair of brackets

		for arg in args:
			if arg == 'g.basic': # append the set you wanted
				sets.append([18.25, 1.4, .1, 1, 2, .2, 1, 4.5, 1, 1, 1, 15, 1])
				continue # go directly to the next iteration without finishing the loop

			subset.append(float(''.join([car for car in arg if car.isnumeric() or car == '.']))) # just extracting the numerical part of the element
			if ']' in arg: #closing a set
				sets.append(subset)
				subset = [] # creating a new one

		output = [*sets[0]] # number of the first set

		for s in sets[1:]: # looping over every other sets
			for i in range(len(s)):
				output[i] *= s[i] # multiplying the numbers together

		await ctx.send(f'{output}')


"""
@commands.check(#fonction) pour checker un truc (fonction return bool)
"""

@bot.event
async def on_ready():
	print('Ready !')

bot.run("Nzk1MzU2MTU2MzEwMzIzMjEx.X_ILJA.bWmivEWYuhZDrwWKFMK9eDDNJlo")