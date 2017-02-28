#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.
import logging
import telegram
import tweepy, time, sys
from telegram.ext import Updater, CommandHandler, Job

CONSUMER_KEY    = 'CONSUMER_KEY' # rellenarlo con la informacion que te proporciona twiter
CONSUMER_SECRET = 'CONSUMER_SECRET' # rellenarlo con la informacion que te proporciona twiter
ACCESS_KEY      = 'ACCESS_KEY' # rellenarlo con la informacion que te proporciona twiter
ACCESS_SECRET   = 'ACCESS_SECRET' # rellenarlo con la informacion que te proporciona twiter
iterator = 0
iterator_two = 0
username = 'carlosmassacubi'
update_id = None
timeline = []
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! this is TTTbot'+"\n http://15809-presscdn-0-93.pagely.netdna-cdn.com/wp-content/uploads/2016/02/MTIyNzYxMTA2MjEyMjkxMTc0.png")
    update.message.reply_text('This are the commands: \n /start \n /update \n /set \n /get_followers\n /get_tweets \n /reload')

def update(bot,update):
    global iterator
    global username 
    global timeline       
    tweets = timeline
    if len(tweets) <= iterator:
        update.message.reply_text("Ya no hay mas tweets cargados")
    else:
        update.message.reply_text(""+tweets[iterator].text+"")
    iterator = iterator +1

def reload(bot,update):
    global iterator
    global iterator_two 
    global timeline 
    timeline = api.home_timeline(screen_name="username",count=200)  
    update.message.reply_text('Uplaod tweets \n Start in the first one now.')
    iterator = 0
    iterator_two = 0

def set(bot, update):
    global username
    global update_id
    chat_id = update.message.chat_id
    username = ""+update.message.text[4:]
    update.message.reply_text('Actualizado a: '+username)

def send_tweet(bot, update):
    chat_id = update.message.chat_id
    if int(11270152) == chat_id:
        api.update_status(update.message.text[6:])                
        update.message.reply_text("Has twiteado: "+update.message.text[6:]+"")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def get_followers(bot,update):
    sleeptime = 4
    pages = tweepy.Cursor(api.followers, screen_name="username").pages()
    while True:
        try:
            page = next(pages)
            time.sleep(sleeptime)
        except tweepy.TweepError: #taking extra care of the "rate limit exceeded"
            time.sleep(60*15) 
            page = next(pages)
        except StopIteration:
            break
        for user in page:
            print(user.id_str)
            update.message.reply_text(""+user.screen_name)
            print(user.followers_count)

def my_tweets(bot,update):
    global iterator_two
    global username
    tweets = api.user_timeline(screen_name = username, count = 20, include_rts = True)
    update.message.reply_text(""+tweets[iterator_two].text+"")
    iterator_two = iterator_two +1

def main():
    updater = Updater('ACCESS_KEY_FOR_TELEGRAM') #Botfather te la dara
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("update", update))
    dp.add_handler(CommandHandler("set", set))
    dp.add_handler(CommandHandler("reload", reload))
    dp.add_handler(CommandHandler("get_followers", get_followers))
    dp.add_handler(CommandHandler("get_tweets", my_tweets))
    dp.add_handler(CommandHandler("tweet", send_tweet))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET);
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET);
    api = tweepy.API(auth);
    main()