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



    
bot.run(token)
