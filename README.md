# WEB SCRAPER

## -- This project is to build a web scraping interface using python. One that will be easy to implement using a GUI

## Creating a Spider

-- In order to create a spider, first access the spider directory from the command line. Then use the following command:

```sh
scrapy genspider {spider_name} {website.com}
```

---

### The Parse Method Inside Our Spider

```sh
    def parse(self, response):
        """this will parse the website data and return whatever data
        we specify using either a css selector or xpath  selector.

        the get() method will return one and getall() returns all the
        specified response tags"""
        # retrieving the title using CSS
        # title = response.css('span.title::text').get()

        # retrieving the title using xpath
        title = response.xpath('//span[@class="title"]/text()').get()

        title = response.xpath()
        return {"title": title}
```

-- Now to run this method use the following command inside the spider directory:

```sh
scrapy runspider {spidername.py}
```

---

## UNDERSTANDING xpath

-- X paths are kind of like the regular expressions of html.

- So if I want to navigate to a particular tag in html I can use:
  - `/html/body/div/h1`
  - This is annoying, because then I have to go through each tag on the page until I get to the h1 tag. So what if I want to just go straight to h1?
- USE A DOUBLE SLASH '//' This will allow me to go directly to whichever tag I list
  `//h1` will grab all the h1 tags

`//div/h1` --> grabs only the h1 tags that are immediate children of the div tag

`//div//h1` --> grabs any h1 tag that falls under a div tag, regardless of whether or not it is an immediate child of the div tag

- Now lets use attribute selection with xpath:
  - Elements are selected by attribute by using the @ symbol:

`//span[@class="title"]` --> Selects any span tags that have the class title or if the attribute of the span tag is equal to the string title

You can also select the text from the attribute of the tags themselves, so if I wanted to select the `id` attribute I would:

- `//span[@class="title"]@id` --> and this will select the value of the id attribute where the class value is title

---

### aa-meetings.com xpath selectors

- xpath to select all the state links: //div[@class="col-md-3 col-6 single-item"]/a

---

## CREATING A CRAWLER

- To do this I will first make a basic crawler for wikipedia.
  - Create the spider by calling `scrapy genspider wikipedia en.wikipedia.org`

1. First, we will extend scrapy's CrawlSpider class:

   - To do this we have to import CrawlSpider from scrapy.spiders and import Rule

```sh
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WikipediaSpider(CrawlSpider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Kevin_Bacon']

    def parse(self, response):
        pass
```

2. Now we need to fill in what we want to extract from each page:

```sh
    def parse(self, response):
        return {
            'title': response.xpath('//h1/text()').get() or response.xpath('//h1/i/text()').get(), # The i is for italicized because movie and article titles are italicized
            'url':response.url,
            'last_edited': response.xpath('//li[@id="footer-info-lastmod"]/text()').get()

        }
```

- Now all we have is something that looks very similar to what the aa spider does. But in order to make a spider a crawler, it needs to have rules. and those rules will guide the spider while it crawls webpages extracting data.

- Below is an example of how to setup a crawlers rules:

```sh
    # -------------------- Create regex pattern to follow correct urls -------------------- #
    url_pattern = 'wiki/((?!:).)*$'

    # ------------------ I need to create rules for the spider to follow ------------------ #
    rules = [Rule(LinkExtractor(allow=url_pattern),
                  callback='parse_info', follow=True)]
```

## STORING SCRAPED DATA

- The easiest way to do this is by adding a few extra commands to the command line:
  `scrapy runspider wikipedia.py -o articles.csv -t csv'
  --> you can also use -t json or xml

- Also, if you want to set a limit to the number of pages to crawl use
  `scrapy runspider wikipedia.py -o articles.csv -t csv -s CLOSESPIDER_PAGECOUNT={num pages}'

## SETTINGS: Creating Custom Settings

> You can create custom settings for each spider by defining the `custom_settings` in the spider class. Some of those settings look like this:

```sh
   custom_settings = {
        'FEED_URI': 'articles.csv',  # This can be json, or xml
        'FEED_FORMAT': 'csv',  # json or xml
        'CLOSESPIDER_PAGECOUNT': 10
    }
```

# Automating LinkedIn Login:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs

def open_firefox():
	driver = webdriver.Firefox()

def login_to_linkedin(driver):
	# Webpage to automate
	driver.get("https://www.linkedin.com/home")
	# get the page title
	title = driver.title

	# make the driver wait 5 seconds
	driver.implicitly_wait(5)

	# Create a text_box element
	user_name = driver.find_element(by=By.ID, value="session_key")
	password = driver.find_element(by=By.ID, value="session_password")

	# Create a submit_button element
	submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button.btn-md:nth-child(3)")

	# send username and password to the text boxes
	user_name.send_keys("cmwolfe1123@gmail.com")
	time.sleep(1)
	password.send_keys("Footb@ll1310")
	time.sleep(2)

	# Submit the form submit button
	submit_button.click()

if __name__ == "__main__":

	# Which driver to use
	driver = webdriver.Firefox()

	# login function
	login_to_linkedin(driver)

	# NOW I NEED TO GET DATA FROM THE LINKED IN PAGE:
	# (I can use BeautifulSoup for this)
	soup = driver.to_soup()
	print(soup.parse_html())

	# Get the message after the click
	# text = text_box.text
	time.sleep(3)
	# Close the driver out
	driver.quit()Just about yeah

```

===============================================================================
## SETTING UP HEADLESS BROWESER FOR SELENIUM IN UBUNTU WSL2 
===============================================================================
##### 1.) INSTALL A HEADLESS BROWSER 
> You can install Firefox or Chrome in headless mode. Headless mode allows you to run the browser without a GUI, which is perfect for server environments and automated scripts like those used in Selenium.

- For Firefox:
```bash
sudo apt update
sudo apt install firefox
```

- For Chrome:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

##### 2.) INSTALL WEBDRIVER
> You'll also need the appropriate WebDriver for your browser.

- For Firefox (Geckodriver)
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux64.tar.gz
tar -xvzf geckodriver-v0.29.0-linux64.tar.gz
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
```

- For Chrome (Chromedriver)
```bash
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

##### 3.) INSTALL SELENIUM
> Ensure that selenium is installed in your Python environment:
```bash
pip install selenium
```

##### 4.) PYTHON SCRIPT EXAMPLE
> Here's a basic Python script example using Selenium with a headless browser.
```python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Set up headless Firefox
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

# Navigate and interact
driver.get("http://example.com")
print(driver.title)

# Clean up
driver.quit()
```

##### 5.) RUN YOUR SCRIPT
> Execute your Python script in the WSL2 environment:

```bash
python3 your_script.py
```

###### Additional Notes:
---
- If you encounter issues with versions or dependencies, make sure to check for compatible versions of the browser, WebDriver, and Selenium.
- Sometimes, running graphical applications in WSL2 might require additional configurations, especially regarding display servers (like X Server), but this is typically not necessary for headless mode.
- Ensure that your WSL2 instance has internet access if your Selenium scripts interact with online resources.

By following these steps, you should be able to run Selenium with a headless browser in a WSL2 Ubuntu environment.

===============================================================================
