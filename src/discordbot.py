import discord
import recommender

import json
import os

client = discord.Client()

if os.getenv("DISCORD_BOT_TOKEN"):
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
else:
    with open("./env.json", mode="r") as f:
        dic = json.loads(f.read())
    TOKEN = dic["DISCORD_BOT_TOKEN"]


@client.event
async def on_ready():
    print("BGA roulette is ready")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/recommend':
        params = {
            'name':'',
            'players':'',
            'best_players':'',
            'mechanism':'',
            'premium':'',
        }
        df = recommender.pickup_games(**params, n=1)
        msg = to_message(df)
        await message.channel.send(msg)

def to_message(df):
    msg = ""
    for row in df.values:
        name, players, best_players, artists, mechanism, premium = row
        msg += f"{name}\nプレイ人数：{players}　（推奨プレイ人数：{best_players}）\nジャンル：{mechanism}\n"
        if premium:
            msg += "このゲームはプレミアム専用だよ"

    return msg

client.run(TOKEN)