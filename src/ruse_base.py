from selenium import webdriver
from bs4 import BeautifulSoup
from redis import Redis
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class RuseBase:
    base_url = 'https://rb.ru'
    news_url = base_url + '/tag/technology/'

    def __init__(self, redis, sender, driver_url):   
        self.driver = webdriver.Remote(command_executor=driver_url, desired_capabilities=DesiredCapabilities.CHROME)
        self.redis = redis
        self.sender = sender

    def parse(self, tags):
        self.driver.get(self.news_url)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        hrefs = [obj.a['href'] for obj in soup.find_all("div", {"class": "news-item"})]
        for href in hrefs:
            self.handle_href(href, tags)
            
    def handle_href(self, href, tags):
        if self.redis.llen("hrefs") and len([i for i in range(0, self.redis.llen("hrefs")) if self.redis.lindex("hrefs", i).decode('utf-8') == href]) > 0:
            return

        if self.validate_href(href, tags):
            self.redis.rpush("hrefs", href)
            self.sender.send_message("New Post!\n"+self.base_url+href)
    
    def validate_href(self, href, tags):
        self.driver.get(self.base_url + href)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        titles = [obj.attrs['title'] for obj in soup.find_all("a", {"class": "mob-menu-list__link"}) if 'title' in obj.attrs]

        return not(set(titles).intersection(set(tags)) == set())