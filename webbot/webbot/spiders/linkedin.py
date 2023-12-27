import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    allowed_domains = ['https://www.linkedin.com/home']
    start_urls = ['https://www.linkedin.com/home/']

    login_data = {'username': 'cmwolfe1123@gmail.com', 'password': ''}
    
    def parse(self, response):
        # page components xpath for user input fields for logging into LinkedIn
        login_username = "//input[@id='session_key']"
        login_password = "//input[@id='session_password']"
        login_submit_button = "//button[@type='submit']"
        title = "//h1[@class='main-heading text-color-text-accent-2 babybear:pb-[24px]']"
        impressions = "//span[normalize-space()='410']"
        reposts = "button[id='ember1208'] span[aria-hidden='true']"
        post_title = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)"
        followers = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)"
        main_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/div[1]/div[1]/img[1]"
        post_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/a[1]/div[1]/div[1]/img[1]"
        submissions = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div[4]/div/div[1]/div[2]/div/div/div/div/div/div/article/div/div[2]/div/a/div/div/div/div/span"
        post_comments = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/ul[1]/li[2]/button[1]/span[1]"
        pass