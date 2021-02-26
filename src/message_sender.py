from telegram import Bot
from redis import Redis

class MessageSender:
    def __init__(self, redis, token):   
        self.redis = redis
        self.bot = Bot(token=token)
    
    def send_message(self, message):
        for i in range(0, self.redis.llen("chats")):
            self.bot.send_message(chat_id=int(self.redis.lindex("chats", i)), text=message)