#!/usr/bin/python3
from scrapy.item import Item , Field
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
import re
class ScrapyItem(Item) :
    Title = Field()
    Price = Field()
    Image = Field()

class ScrapySpider(Spider) :
    name = 'base'
    cost = ""
    allowed_domain = ["ralphlauren.com"]
    start_urls = ["http://www.ralphlauren.com/family/index.jsp?categoryId=2004212&cp=1760781&ab=ln_men_cs_dressshirts"]
    def parse(self , response) :
        select = Selector(response)
        item = ScrapyItem()
        products = select.xpath("//*/dl/dt/a[2]/text()").extract()
        products = [product.strip() for product in products]
        cost = select.xpath("//*/dl/dd[1]/div/span/nobr/a/text()").extract()
        amounts = [i.split(': ')[1] for i in cost]
        amounts = [amount.strip() for amount in amounts]
        img_urls = select.xpath("//div[re:test(@id, 'staticImg\d+')]//a/img/@data-blzsrc").extract()
        img_urls = [img_url.strip() for img_url in img_urls]
        output = zip(products , amounts , img_urls)
        for product , amount , img_url in output :
            item['Title'] = product
            item['Price'] = amount
            item['Image'] = img_url
            yield item
def main() :
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' , 'FEED_FORMAT': 'csv' , 'FEED_URI': 'RLlist.csv'})
    process.crawl(ScrapySpider)
    process.start()
if __name__ == '__main__' : main()
