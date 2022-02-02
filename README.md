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

## UNDERSTANDING xpath:

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

### aa-meetings.com xpath selectors:

- xpath to select all the state links: //div[@class="col-md-3 col-6 single-item"]/a
