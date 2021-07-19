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
	brief="Prints pong back to the channel."
)
async def ping(ctx):
	# SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.
	await ctx.channel.send("pong")
    
@bot.command()
async def neko(ctx):
    await ctx.send('にゃーん')

@bot.command()
async def ok(ctx):
    sent_msg = await ctx.send(f"OK?")    
    await sent_msg.add_reaction('⭕')
    await sent_msg.add_reaction('❌')
    
@bot.command()
async def vote2(ctx):
    sent_msg = await ctx.send(f"OK?")    
    await sent_msg.add_reaction('🅰')
    await sent_msg.add_reaction('🅱')
    
@bot.command()
async def on_message(message):

    #メッセージを送信する
    if message.content.startswith('/send_dm '):

        # DMに送るメッセージを取得
        msg = message.content.replace('/send_dm ', '')

        # コマンドを打った人のDMに送信
        await message.author.send(msg)
        # message.author はメッセージを送信したユーザーです
    
    # Embedメッセージを送信する
    elif message.content.startswith('/send_embed'):

        # Embedメッセージ
        embed_msg = discord.Embed(title="Embedメッセージ", description="正常に送信されました")

        # コマンドを打った人のDMに送信
        await message.author.send(embed=embed_msg)
    
    # ファイルを送信する
    elif message.content.startswith('/send_file'):
        
        # コマンドを打った人のDMに送信
        await message.author.send(content='ファイル送信', file=discord.File('test.txt'))
        # discord.File()には、送信したいファイルの名前やファイルパスを入れます。
        # 例) 'image.jpg', './image/1.png', 'data.txt' など
    
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
