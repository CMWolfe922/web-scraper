import scrapy


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
        pass