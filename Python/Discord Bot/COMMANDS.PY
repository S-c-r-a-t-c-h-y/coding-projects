rver.member_count
	name = server.name
	await ctx.send(f'The **{name}** server has currently *{nb_members}* members.\n \
	It has a total of {nb_text_channels} text channels and {nb_voice_channels} voice channels.\n\
	The description is "{desc}".')
list_commands.append(server_info)

""" ---------- moderations commands ---------- """

@bot.command()
@commands.guild_only()
async def ban(ctx, user: discord.user, *reason):
	await ctx.guild.ban(user, "".join(reason))
	await ctx.send(f'{user} has been banned for the reason : *{"".join(reason)}*.')
list_commands.append(ban)


@bot.command()
@commands.guild_only()
async def unban(ctx, user, *reason):
	user_name, user_id = user.split('#')
	banned_users = await ctx.guild.bans()
	for banned_user in banned_users:
		if banned_user.user.name == user_name and banned_user.user.discriminator == user_id:
			await ctx.guild.unban(user, "".join(reason))
			await ctx.send(f'{user} has been unbanned for the reason : *{"".join(reason)}*.')
			return
	await ctx.send('I could not find the user you were searching for ...')
list_commands.append(unban)


@bot.command()
@commands.guild_only()
async def kick(ctx, user: discord.User, *reason):
	await ctx.guild.kick(user, reason="".join(reason))
	await ctx.send(f'{user} has been kicked for the reason : *{"".join(reason)}*.')
list_commands.append(kick)


@bot.command()
async def clear(ctx, nb: int):
	messages = await ctx.channel.history(limit=nb+1).flatten()
	for mess in messages:
		await mess.delete()
	await ctx.send(f'{nb} messages has been deleted.')
list_commands.append(clear)                                                                                                                                                                                                                                                                                                                                                                                                                                               ��d��S�qW��U�xkW�S� w�WP'�zw:�+<������3�I�v��o����Oַ�H�ދ�׷cqc�X