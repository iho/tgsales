import time
from datetime import datetime
from time import mktime

import feedparser
from pymongo import MongoClient, ReturnDocument

import bot

bot.db
bot.posts

BUILDAPCSALES = "buildapcsales"
GAMEDEALS = "gamedeals"


def broadcast(entry, broadcast_type=BUILDAPCSALES):
    text = entry["title"] + "\n\n" + entry["link"]

    for user in bot.db.find({broadcast_type: True}):
        print(user["_id"])
        bot.updater.bot.send_message(user["_id"], text)


def check_subreddit(url, type_):
    news_feed = feedparser.parse(url)
    entry = news_feed.entries[0]
    date = datetime.fromtimestamp(mktime(entry["updated_parsed"]))
    res = bot.db.find_one_and_update(
        {"_id": type_},
        {"$set": {"last_update": date}},
        upsert=True,
        return_document=ReturnDocument.BEFORE,
    )
    print(res)
    if date > res.get("last_update", date):
        broadcast(entry, broadcast_type=type_)


while True:
    try:
        check_subreddit("https://www.reddit.com/r/GameDeals/new/.rss", GAMEDEALS)

    except Exception as e:
        print(e)
    try:
        check_subreddit("https://www.reddit.com/r/buildapcsales/new/.rss", BUILDAPCSALES)
    except Exception as e:
        print(e)

    time.sleep(60)
