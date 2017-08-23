import scrapy
from scrapy.exceptions import CloseSpider

class IrnaSpider(scrapy.Spider):
    name = 'irna'
    base_url = 'http://www.irna.ir/en/services/161'
    next_page = 162


    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):

        for article_url in response.css('.DataListContainer h3 a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1
        if response.css('#MoreButton'):
            yield scrapy.Request('{}/page{}'.format(self.base_url, page_number),
                callback=self.parse, meta={'page_number': page_number})

        for next_article in ('/en/services/162/', '/en/services/163/', '/en/services/164/'):
            yield response.follow(next_article, callback=self.parse)


    def parse_article(self, response):
        with open("irnadate.txt", "rt") as in_file:
            irnadate = in_file.read()

        articledate = ''.join(response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent4_NofaDateLabel2"]/text()').re(r'(.*)/(.*)/(.*)'))
        articletime = ''.join(response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent4_NofaDateLabel3"]/text()').re(r'(.*):(.*)'))
        articlestamp = articledate + articletime

        articlestampint = int(articlestamp)
        irnadateint = int(irnadate)

        if articlestampint <= irnadateint:
            raise CloseSpider('duplicate article')

        yield {
            'date': ''.join(response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent4_NofaDateLabel2"]/text()').re(r'(.*)/(.*)/(.*)')),
            'time': ''.join(response.xpath('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent4_NofaDateLabel3"]/text()').re(r'(.*):(.*)')),
            'title': ''.join(response.xpath('//*[@id="col-3"]/div/div[1]/div/h1/text()').extract_first()),
            'text': ''.join(response.xpath('//p[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_NewsContent4_BodyLabel"]/text()').extract()),
            'tags': [tag.strip() for tag in response.xpath('//div[@class="Tags"]/p/a/text()').extract() if tag.strip()]

        }
