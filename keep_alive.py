from flask import Flask
from threading import Thread
import os

"""
Renderの無料枠でBotを動かす場合、「Webサイトとしての機能（アクセスできるページ）を持たせないと、エラーだと勘違いされて強制終了させられてしまう」というルールがある。
→これを回避するために、Botの中に「極小のWebサーバー」を組み込んで、Renderを安心させるコードを追加。
"""

app = Flask('')

@app.route('/')
def home():
    return "maho-info is running!"

def run():
    # Renderから割り当てられるポート番号を取得し、なければ8080を使う
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
