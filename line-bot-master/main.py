import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
with open('info.json', 'r') as f:
    info = json.load(f)
CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
USER_ID = info['USER_ID']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
def main():
    USER_ID = info['USER_ID']
    messages = TextSendMessage(text="今日の経過報告お願い")
    line_bot_api.push_message(USER_ID,messages=messages)

if __name__=="__main__":
    main()