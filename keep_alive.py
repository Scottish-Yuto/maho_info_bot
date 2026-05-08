from flask import Flask
from threading import Thread

"""
Renderの無料枠でBotを動かす場合、「Webサイトとしての機能（アクセスできるページ）を持たせないと、エラーだと勘違いされて強制終了させられてしまう」というルールがある。
→これを回避するために、Botの中に「極小のWebサーバー」を組み込んで、Renderを安心させるコードを追加。
"""

app = Flask('')

@app.route('/')
def home():
    return "maho-info is running!"

def run():
    # Renderが指定するポートで待機します
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()