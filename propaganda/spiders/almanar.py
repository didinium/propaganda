import scrapy

class AlmanarSpider(scrapy.Spider):
    name = 'almanar'
    base_url = 'https://english.almanar.com.lb/cat/news'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('//*[@id="main"]/div/div//@href').re(r'https://english.almanar.com.lb/\d\d+'):
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'https://english.almanar.com.lb/cat/news/page/' + str(page_number)

        if page_number is not 581:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})

            print("\n\n%d", new_url)



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//*[@id="main"]/div/div/div//span[2]/text()[2]').extract_first()),
            'title': ''.join(response.xpath('//*[@id="main"]/div/div/div//h2/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="main"]/div/div//div[6]/p/text()').extract()),
            }
