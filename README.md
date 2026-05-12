# 映画ニュース自動取得Bot
## 〇概要
映画研究サークル「mahoroba」のDiscordサーバーに、最新の映画ニュースを自動で配信するBotです。邦画・洋画の最新情報を定期的に巡回し、新しい記事が公開されたタイミングでDiscordに通知します。
## 〇機能
- **複数メディアの自動巡回**：1時間ごとに指定したRSSフィードを確認します
- **重複投稿防止**：サイトごとに最後に投稿したURLを記憶しておき、同じ記事が通知されないようになっています
- **ランダムメッセージ**：投稿時の挨拶を複数パターンからランダムに選択し、単調にならないよう演出しています
- **24時間稼働**：keep_alive.pyを用い、24時間記事を確認するよう設計しています
## 〇使用技術
- Python 3.x
- discord.py：Discord APIラッパー
- feedparser：RSSフィードの解析
- Flask：常時稼働用の軽量Webサーバー
## 〇環境構築
### 1.依存アプリのインストール
pip install discord.py feedparser flask
### 2.環境変数の設定
セキュリティのため、Botのトークンを環境変数として設定：DISCORD_TOKEN
### 3.設定のカスタマイズ
- CHANNEL_ID：ニュースを流したいDiscordチャンネルのID
- RSS_URLS：取得したいニュースサイトのRSSフィードURL
- MESSAGES：投稿時にランダムで選ばれるメッセージ
## 〇ファイル構成
- mahoinfo_bot.py：Botのメインプログラム
- keep_alive.py：24時間稼働用の簡易Webサーバープログラム
- requirements.txt：必要なPythonライブラリの一覧
## 〇情報取得元
- [映画ナタリー](https://natalie.mu/eiga/)
- [THE RIVER](https://theriver.jp/)
