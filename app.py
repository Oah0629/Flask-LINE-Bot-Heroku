import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    if input_text == "$疫情":
        url = 'https://attach.setn.com/data/dynamic/covid19.json'
        html = requests.get(url).text
        data = json.loads(html)  # 轉為字典
        data1 = list(data["data_1"]["mainData"][0].values())
        data2 = list(data["data_1"]["mainData"][1].values())
        data3 = list(data["data_1"]["mainData"][2].values())
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"本土：{data1[1]}"+"\n"+f"境外：{data2[1]}"+"\n"+f"死亡：{data3[1]}"+"\n"+data["data_1"]["bottomRemarks"]))

