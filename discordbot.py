from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

 if message.content == "!投票":
        # リアクションアイコンを付けたい
        q = await message.channel.send("あなたは右利きですか？")
        [await q.add_reaction(i) for i in ('⭕', '❌')]  # for文の内包表記

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
@bot.command()
async def neko(ctx):
    await ctx.send('にゃーん')


        
bot.run(token)
