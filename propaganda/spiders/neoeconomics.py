import scrapy

class NeoeconomicsSpider(scrapy.Spider):
    name = 'neoeconomics'
    base_url = 'https://journal-neo.org/category/columns/economics/'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('/html/body/div[2]/div[1]/div[1]/div[1]/div[2]//@href').re(r'.+org/\d.+'):
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'https://journal-neo.org/category/columns/politics/page/' + str(page_number)

        if page_number is not 51:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})

            print("\n\n%d", new_url)



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('/html/body/div[2]//div[1]/span[1]/text()').extract_first()),
            'title': ''.join(response.xpath('/html/body/div[2]/div[1]//header/h1/text()').extract_first()),
            'text': ''.join(response.xpath('/html/body/div[2]/div[1]//div[4]//text()').extract())
            }
