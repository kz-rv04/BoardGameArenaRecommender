import discord
from discord.ext import commands
import recommender

import json
import os

bot = commands.Bot(command_prefix=".bga ")
activity = discord.Game(".bga help")

if os.getenv("DISCORD_BOT_TOKEN"):
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
else:
    with open("./env.json", mode="r") as f:
        dic = json.loads(f.read())
    TOKEN = dic["DISCORD_BOT_TOKEN"]



#### bot command
@bot.event
async def on_ready():
    print("BGA recommend is ready")
    await bot.change_presence(activity=activity)

@bot.command(name="recommend")
async def recommend(ctx, *args):
    """recommends random game
    ex).bga recommend name=宝石 players=4 best_players=4 mechanism=競り
    Args: `name`：ゲーム名を部分一致で検索します
          `players`：プレイ可能な人数で絞り込みます
          `best_players`：最適なプレイ人数で絞り込みます
          `mechanism`：ゲームのメカニズムで絞り込みます（.bga mechanismでコマンドの一覧を表示します）
          `premium`：プレミアム限定のゲームで絞り込みます（0:無料 1:プレミアム）
    """
    if ctx.author.bot:
        return
    params = {
        'name':'',
        'players':'',
        'best_players':'',
        'mechanism':'',
        'premium':'',
    }
    if args:
        params = parse_args(args)
    print(params)
    df = recommender.pickup_games(**params, n=1)
    # ゲームが1件も取得できなかった場合
    if df.empty:
        await ctx.channel.send("ゲームが見つかりませんでした")
        return

    msg = to_message(df)
    await ctx.channel.send(msg)

@bot.command(name="mechanism")
async def mechanism(ctx):
    """list all game mechanisms"""
    if ctx.author.bot:
        return
    await ctx.channel.send('```{msg}```'.format(msg='\n'.join(sorted(recommender.get_tag_list()))))

def to_message(df):
    msg = ""
    for row in df.values:
        name, players, best_players, artists, mechanism, premium = row
        msg += f"{name}\nプレイ人数：{players}　（推奨プレイ人数：{best_players}）\nジャンル：{mechanism}\n"
        if premium:
            msg += "このゲームはプレミアム専用だよ"

    return msg

def parse_args(args):
    params = {
        'name':'',
        'players':'',
        'best_players':'',
        'mechanism':'',
        'premium':'',
    }
    for arg in args:
        k, v = arg.split('=')
        if not (k and v):
            continue
        if not k in params.keys():
            continue
        params[k]=v
    return params

bot.run(TOKEN)