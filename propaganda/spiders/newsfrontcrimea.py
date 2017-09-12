import scrapy

class NewsfrontcrimeaSpider(scrapy.Spider):
    name = 'newsfrontcrimea'
    base_url = 'https://en.news-front.info/category/ukraine/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('//div/div[2]/div[2]/a/@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'https://en.news-front.info/category/ukraine/page/' + str(page_number)

        if page_number is not 31:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//header/p').re(r'\d\d \d\d \d\d\d\d')),
            'time': ''.join(response.xpath('//header/p').re(r'\d\d:\d\d')),
            'title': ''.join(response.xpath('//header/h1/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="content"]/div/p/span/text()').extract())
            }
