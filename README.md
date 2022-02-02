# WEB SCRAPER

-- This project is to build a web scraping interface using python. One that will be easy to implement using a GUI.

## Creating a Spider:

-- In order to create a spider, first access the spider directory from the command line. Then use the following command:

```sh
scrapy genspider {spider_name} {website.com}
```

### The Parse Method Inside Our Spider:

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
