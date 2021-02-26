from redis import Redis
from ruse_base import RuseBase
from message_sender import MessageSender
import os

redis_url = os.environ.get('REDIS_URL')
redis_port = os.environ.get('REDIS_PORT')
telegram_token = os.environ.get('TELEGRAM_TOKEN')
driver_url = os.environ.get('DRIVER_URL')

redis = Redis(host=redis_url, port=redis_port)

def main():
    sender = MessageSender(redis, telegram_token)
    rusbase = RuseBase(redis, sender, driver_url)
    rusbase.parse(["Технологии", "Бизнес"])
    

if __name__ == "__main__":
    main()