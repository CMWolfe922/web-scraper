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
