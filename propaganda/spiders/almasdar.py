import scrapy

class AlmasdarSpider(scrapy.Spider):
    name = 'almasdar'
    base_url = 'https://www.almasdarnews.com/article/category/syria/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('//*[@id="td-outer-wrap"]/div[4]/div/div/div[1]/div//h3/a/@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'https://www.almasdarnews.com/article/category/syria/page/' + str(page_number)

        if page_number is not 1154:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//div[1]/div/div/header/div/span/time/@datetime').re(r'\d\d\d\d-\d\d-\d\d')),
            'title': ''.join(response.xpath('//div[1]/div/div/header/h1/text()').extract()),
            'text': ''.join(response.xpath('//div[2]/div[1]/div/div[1]/p/text()').extract())
            }
