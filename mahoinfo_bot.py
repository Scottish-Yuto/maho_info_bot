import discord
from discord.ext import tasks
import feedparser
import time
from keep_alive import keep_alive
import os

# --- 設定 ---
# トークンを直接書かず、環境変数から読み込む
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1502220617208823859  # ニュースを流したいチャンネルのID
RSS_URLS = [
    'https://natalie.mu/eiga/feed/news',
    'https://natalie.mu/eiga/feed/column'
]

# 最後に取得した記事のURLを保存する変数（重複投稿防止）
last_posted_link = ""

# Discordクライアントの準備
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    # Bot起動時に定期実行タスクをスタート
    fetch_news.start()

# 1時間(3600秒)ごとに実行されるタスク
@tasks.loop(seconds=3600)
async def fetch_news():
    global last_posted_link
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # forループで、リストに書いたURLを1つずつ順番に処理する
    for url in RSS_URLS:
        feed = feedparser.parse(url)
    
        if feed.entries:
            # 一番新しい記事（リストの先頭）を取得
            latest_entry = feed.entries[0]
            
            # 前回の記事とURLが違えば、新しいニュースと判定して投稿
            if latest_entry.link != last_posted_link:
                msg = f"🎬 **最新の映画ニュースが届きました！**\n{latest_entry.title}\n{latest_entry.link}"
                await channel.send(msg)
                # 最後に投稿したURLを更新
                last_posted_link = latest_entry.link

# Botを実行する直前に、Webサーバーを起動して命綱を繋ぐ
keep_alive() 
client.run(TOKEN)

# Botの実行
client.run(TOKEN)
