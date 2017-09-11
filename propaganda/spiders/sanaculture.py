import scrapy

class SanacultureSpider(scrapy.Spider):
    name = 'sanaculture'
    base_url = 'http://sana.sy/en/?cat=8'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('//*[@id="main-content"]/div[1]/div[2]/div/div/ul/li[1]/div[1]/h2/a/@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'http://sana.sy/en/?cat=8&paged=' + str(page_number)

        if page_number is not 51:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//*[@id="main-content"]/div[1]/h1/span/text()').extract_first()),
            'title': ''.join(response.xpath('//*[@id="the-post"]/div[2]/p/span/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="the-post"]/div[2]/div[2]/p/text()').extract())
            }
