import discord
from discord.ext import tasks
import feedparser
import time
from keep_alive import keep_alive
import os
import random

# --- 設定 ---
# トークンを直接書かず、環境変数から読み込む
TOKEN = os.getenv('DISCORD_TOKEN')
# ニュースを流したいチャンネルのID
CHANNEL_ID = 1502220617208823859
# サイトのRSS
RSS_URLS = [
    'https://natalie.mu/eiga/feed/news',
    'https://theriver.jp/feed/'
]
# メッセージのパターン
MESSAGES = [
    "🎬 **最新の映画ニュースが届きました！**",
    "🎥 **話題の映画情報！**",
    "🍿 **気になるニュースをチェック！**",
    "🌟 **【新着】映画ニュース**",
    "📢 **最新記事が公開されました！**"
]
# 最後に取得した記事のURLを保存する変数（重複投稿防止）
last_posted_links = {}
# Discordクライアントの準備
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    # Bot起動時に、現在の各サイトの最新記事を記憶（起動時の連騰を防止）
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        if feed.entries:
            last_posted_links[url] = feed.entries[0].link
    # ループが動いていなければ開始
    if not fetch_news.is_running():
        fetch_news.start()

# 1時間(3600秒)ごとに実行されるタスク
@tasks.loop(seconds=3600)
async def fetch_news():
    global last_posted_links
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    if channel is None:
        return
        
    # forループで、リストに書いたURLを1つずつ順番に処理する
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        
        if feed.entries:
            # 一番新しい記事（リストの先頭）を取得
            latest_entry = feed.entries[0]
            current_link = latest_entry.link
            
            # 前回と違うURL、かつ未記録のサイトなら投稿
            prev_link = last_posted_links.get(url)
            if current_link != prev_link:
                prefix = random.choice(MESSAGES)
                msg = f"{prefix}\n{latest_entry.title}\n{current_link}"
                await channel.send(msg)
                # 最後に投稿したURLを更新
                last_posted_links[url] = current_link

# Botを実行する直前に、Webサーバーを起動して命綱を繋ぐ
keep_alive()
# Botの実行
client.run(TOKEN)
