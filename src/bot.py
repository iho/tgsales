import logging
import os
import tempfile
from datetime import datetime, timedelta

import telegram
from pymongo import MongoClient, ReturnDocument
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

pcsales_bot = MongoClient("localhost", 27017).pcsales_bot
db = pcsales_bot.users
posts = pcsales_bot.posts

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

greeting_message = """
Welcome to PC sales bot!
Available commands:
/start
/enable_all
/enable_buildapcsales
/enable_gamedeals
/disable_buildapcsales
/disable_gamedeals
/mute_all
"""


def enable_all(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"buildapcsales": True, "gamedeals": True}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Subscribed to two subreddits!",
    )


def enable_buildapcsales(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"buildapcsales": True}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Subscribed to buildapcsales!",
    )


def enable_gamedeals(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"gamedeals": True}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Subscribed to gamedeals!",
    )


def disable_buildapcsales(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"buildapcsales": False}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Unsubscribed to buildapcsales!",
    )


def disable_gamedeals(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"gamedeals": False}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Unsubscribed to gamedeals!",
    )


def mute_all(update, context):
    chat_id = update.effective_chat.id
    res = db.find_one_and_update(
        {"_id": chat_id},
        {"$set": {"gamedeals": False, "buildapcsales": False}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    print(res)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="All muted!",
    )


def start_handler(update, context):

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=greeting_message,
        parse_mode=ParseMode.HTML,
    )
    # custom_keyboard = [
    #     ['/enable_buildapcsales', 'top-right'],
    #                ['bottom-left', 'bottom-right']]
    # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    # context.bot.send_message(chat_id=update.effective_chat.id,
    #              text="Custom Keyboard Test",
    #              reply_markup=reply_markup)


TOKEN = os.getenv("TOKEN")
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start_handler))
dispatcher.add_handler(CommandHandler("enable_all", enable_all))
dispatcher.add_handler(CommandHandler("enable_buildapcsales", enable_buildapcsales))
dispatcher.add_handler(CommandHandler("enable_gamedeals", enable_gamedeals))
dispatcher.add_handler(CommandHandler("disable_buildapcsales", disable_buildapcsales))
dispatcher.add_handler(CommandHandler("disable_gamedeals", disable_gamedeals))
dispatcher.add_handler(CommandHandler("mute_all", mute_all))


if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
