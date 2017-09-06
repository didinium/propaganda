import scrapy

class ChinadailySpider(scrapy.Spider):
    name = 'chinadaily'
    base_url = 'http://usa.chinadaily.com.cn/us/index.html'

    def start_requests(self):
        yield scrapy.Request(self.base_url, meta={'page_number': 1})

    def parse(self, response):
        for article_url in response.xpath('/html/body/div[4]/div[1]/div[1]/span/h4/a/@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'http://usa.chinadaily.com.cn/us/index_' + str(page_number) + '.html'

        if page_number is not 21:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})

            print("\n\n%d", new_url)



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('/html/body/div[4]/div[1]/div[1]/span[1]').re(r'\d\d\d\d-\d\d-\d\d')),
            'time': ''.join(response.xpath('/html/body/div[4]/div[1]/div[1]/span[1]').re(r'\d\d:\d\d')),
            'title': ''.join(response.xpath('/html/body/div[4]/div[1]/h1/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="Content"]/p/text()').extract())
            }
