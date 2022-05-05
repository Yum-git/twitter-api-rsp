import json
import os

# .envファイルに環境変数を書き込んでいる時のみ利用する
# 利用しない時は削除してもいい
from dotenv import load_dotenv
load_dotenv()

CK = os.getenv("CONSUMER_KEY")
CS = os.getenv("CONSUMER_SECRET")
AT = os.getenv("ACCESS_TOKEN")
ATS = os.getenv("ACCESS_TOKEN_SECRET")
BT = os.getenv("BEARER_TOKEN")

TWITTER_ID = os.getenv("TWITTER_ID")

import tweepy

Client = tweepy.Client(BT, CK, CS, AT, ATS)

user_id_list = []

class ClientProcess(tweepy.StreamingClient):
    def on_data(self, raw_data):
        response = json.loads(raw_data)
        tweet_id = response["data"]["id"]
        reply_text: str = response["data"]["text"]

        user_id = response["matching_rules"][0]["id"]

        if user_id not in user_id_list:
            text_list = reply_text.split()
            if "#グーを出す" in text_list:
                text = "残念、Botの勝利！ \nhttps://youtu.be/LhPJcvJLNEA"
            elif "#パーを出す" in text_list:
                text = "残念、Botの勝利！　\nhttps://youtu.be/28d78XP1TJs"
            elif "#チョキを出す" in text_list:
                text = "残念、Botの勝利！　\nhttps://youtu.be/SWNCYpeDTfo"
            else:
                return
            Client.create_tweet(
                text=text,
                in_reply_to_tweet_id=tweet_id
            )

            user_id_list.append(user_id)

        return


def main():
    printer = ClientProcess(BT)
    printer.add_rules(tweepy.StreamRule(TWITTER_ID))
    printer.filter()

if __name__ == '__main__':
    main()
