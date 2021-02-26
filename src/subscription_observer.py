from telegram.ext import Updater, CommandHandler, Filters, CallbackContext
from telegram import Update
from redis import Redis

class SubscriptionObserver:
    def __init__(self, redis, token):   
        self.redis = redis
        self.updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler("start", self.handler))
        
    def start(self):
        self.updater.start_polling()

    def handler(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Hi!')
        print('**************************')
        print(update.effective_chat.id)

        self.redis.rpush("chats", update.effective_chat.id)
