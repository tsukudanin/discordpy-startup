from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='$')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command(
	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
	help="Uses come crazy logic to determine if pong is actually the correct value or not.",
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="botがpongと発言します。"
)
async def ping(ctx):
	# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
	await ctx.channel.send("pong")
    
@bot.command(
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="何処からかにゃーんと声が…"
)
async def neko(ctx):
    await ctx.send('にゃーん')

@bot.command(
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="〇と×で投票できます。"
)
async def ok(ctx):
    sent_msg = await ctx.send(f"これで良い?")    
    await sent_msg.add_reaction('⭕')
    await sent_msg.add_reaction('❌')
    
@bot.command(
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="AとBの二択の投票ができます。"
)
async def vote2(ctx):
    sent_msg = await ctx.send(f"どっちにする?")    
    await sent_msg.add_reaction('🅰')
    await sent_msg.add_reaction('🅱')
    
    
@bot.command(
	# ADDS THIS VALUE TO THE $HELP MESSAGE.
	brief="三原色で三択の投票ができます。"
)
async def vote2(ctx):
    sent_msg = await ctx.send(f"どれにする?")    
    await sent_msg.add_reaction('🔴')
    await sent_msg.add_reaction('🔵')
    await sent_msg.add_reaction('🟡')

@bot.command()
async def member(ctx, day: int):
    if ctx.message.author.nick is not None:
        name = ctx.message.author.nick
    else:
        name = ctx.message.author.name
    sent_msg = await ctx.send(f"day: {day}, name: {name} OK?")
    await sent_msg.add_reaction('👍')

    def check(reaction, user):
        are_same_messages = reaction.message.channel == sent_msg.channel and reaction.message.id == sent_msg.id
        return user == ctx.message.author and str(reaction.emoji) == '👍'  and are_same_messages

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('タイムアウトになりました。もう一度コマンドを入力し直してください')
    else:
        await ctx.send('記入しました')

    
bot.run(token)
