from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from gpt_module import extract_expense_data
from sheet_module import append_to_sheet
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 使用者分段資料暫存
session_store = {}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text.strip()

    # Step 1: 收金額
    if user_id not in session_store:
        if user_text.isdigit():
            session_store[user_id] = {"金額": user_text}
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="📌 收到了金額～現在請你用一句話說說消費時的心情或想法吧～")
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請先輸入消費金額（例如：300）～")
            )
        return

    # Step 2: 收心情文字
    if user_id in session_store and "情緒敘述" not in session_store[user_id]:
        if len(user_text) < 5 or user_text.lower() in ["好", "還行", "ok"]:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請用一句話告訴我你當時的心情！越真實越好唷 🥹")
            )
            return

        session_store[user_id]["情緒敘述"] = user_text
        combined_text = user_text + f"，花了 {session_store[user_id]['金額']} 元"
        analysis = extract_expense_data(combined_text)
        append_to_sheet(combined_text, analysis, user_id)
        reply = f"✅ 已記錄：{analysis['金額']} 元｜分類：{analysis['類別']}｜情緒：{analysis['情緒']}"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
        del session_store[user_id]
        return
