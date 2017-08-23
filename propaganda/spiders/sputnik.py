import scrapy

class SputnikSpider(scrapy.Spider):
    name = 'sputnik'
    base_url = 'https://sputniknews.com/world/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.css('.b-stories__title h2 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)
        
        more_button = response.xpath('//*[@id="rubric-major"]/div[2]/a/@href').extract_first()
        if more_button is not None:
            yield response.follow(more_button, callback=self.parse)

        for next_article in ('/business/', '/politics/', '/analysis/', '/art_living/', '/science/'):
            yield response.follow(next_article, callback=self.parse)




    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('/html/body/div[8]/div[1]/div/div[1]/div[1]/time[1]/text()').re(r' (.*)\.(.*)\.(.*)')),
            'time': ''.join(response.xpath('/html/body/div[8]/div[1]/div/div[1]/div[1]/time[1]/text()').re(r'(.*):(.*) ')),
            'title': ''.join(response.xpath('/html/body/div[7]/div/div/div[1]/h1/text()').extract_first()),
            'text': ''.join(response.xpath('/html/body/div[8]/div[1]/div/div[3]/p/text()').extract()),
            'tags': [tag.strip() for tag in response.xpath('/html/body/div[8]/div[1]/div/div[9]/div[3]/div/div[2]').re(r'>(\S+)</a>') if tag.strip()]
        }
