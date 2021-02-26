from redis import Redis
from subscription_observer import SubscriptionObserver
import os

redis_url = os.environ.get('REDIS_URL')
redis_port = os.environ.get('REDIS_PORT')
telegram_token = os.environ.get('TELEGRAM_TOKEN')

redis = Redis(host=redis_url, port=redis_port)

def main():
    observer = SubscriptionObserver(redis, telegram_token)
    observer.start()

if __name__ == "__main__":
    main()
