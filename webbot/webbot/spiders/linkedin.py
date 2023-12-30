import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import settings
from scrapy.http import FormRequest


class LinkedinSpider(scrapy.Spider):
    name = 'linkedin'
    login_url = "https://www.linkedin.com/home"
    start_urls = [login_url]

    login_input_xpath = "//input[@id='session_key']",
    login_password_input_xpath = "//input[@id='session_password']",
    login_submit_button_xpath = "//button[@type='submit']",

    def parse(self, response):
        # Extract any additional form fields or tokens if needed
        # csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()

        # Define your login credentials
        username = self.settings.get('LINKEDIN_USERNAME')
        password = self.settings.get('LINKEDIN_PASSWORD')

        # Fill in the login form fields
        yield FormRequest.from_response(
            response,
            formdata={
                self.login_input_xpath: username,
                self.login_password_input_xpath: password,
                # 'csrf_token_field_name': csrf_token,  # Include if needed
                # Add any other required form fields here
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # Check if the login was successful
        if "Welcome, " in response.text:
            self.logger.info("Login successful")
            # You can continue with your scraping logic here
            # For example, you can yield requests to other pages you want to scrape
            yield self.parse_feed(response)
            
        else:
            self.logger.error("Login failed")

    def parse_feed(self, response):
        # Extract data from the feed page and do something with it
        title = "//h1[@class='main-heading text-color-text-accent-2 babybear:pb-[24px]'].text()"
        impressions = "//span[normalize-space()='410'].text()"
        reposts = "button[id='ember1208'] span[aria-hidden='true'].text()"
        post_title = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(1)"
        followers = "body > div:nth-child(65) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > main:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)"
        main_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/a[1]/span[1]/div[1]/div[1]/img[1]"
        post_image = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/article[1]/div[1]/div[1]/a[1]/div[1]/div[1]/img[1]"
        submissions = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/div[4]/div/div[1]/div[2]/div/div/div/div/div/div/article/div/div[2]/div/a/div/div/div/div/span"
        post_comments = "/html[1]/body[1]/div[5]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/main[1]/div[4]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[1]/div[1]/ul[1]/li[2]/button[1]/span[1]"
        
        data = {
            'title': response.xpath(title).get(),
            'impressions': response.xpath(impressions).get(),
            'reposts': response.css(reposts).get(),
            'post_title': response.css(post_title).get(),
            'followers': response.css(followers).get(),
            'main_image': response.xpath(main_image).get(),
            'post_image': response.xpath(post_image).get(),
            'submissions': response.xpath(submissions).get(),
            'post_comments': response.xpath(post_comments).get(), 
        }
        yield data
        
