import scrapy

class RtSpider(scrapy.Spider):
    name = 'rt'
    base_url = 'https://www.rt.com/usa/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.css('.js-listing strong a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        more_button = response.xpath('/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[5]/div/div/div/a/@href').extract_first()
        if more_button is not None:
            yield response.follow(more_button, callback=self.parse)

        for next_article in ('/uk/', '/politics/', '/business/', '/sport/', '/op-edge/'):
            yield response.follow(next_article, callback=self.parse)




    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div/div[3]/time[1]/text()').re(r': (.*) ..:')),
            'time': ''.join(response.xpath('/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div/div[3]/time[1]/text()').re(r'(\d\d:\d\d)')),
            'title': ''.join(response.xpath('/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div/h1/text()').extract_first()),
            'text': ''.join(response.xpath('string(/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div/div[8])').extract()),
        }
