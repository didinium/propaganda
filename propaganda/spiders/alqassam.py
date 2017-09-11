import scrapy, cfscrape

class AlqassamSpider(scrapy.Spider):
    name = 'alqassam'
    base_url = ['http://www.qassam.ps/news-archive.html']

    def start_requests(self):
        cf_requests = []
        for url in self.base_url:
        #yield scrapy.Request(self.base_url, meta={'page_number': 1})
            cf_requests.append(scrapy.Request(url=url,
                #cookies={'__cfduid': token['__cfduid']},
                #headers={'User-Agent': agent},
                meta={'page_number': 1}))
            return cf_requests

    def parse(self, response):
        for article_url in response.xpath('//*[@id="col3_content"]/div[2]/ul//a/@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        page_number = response.meta['page_number'] + 1

        new_url = 'http://www.qassam.ps/news-archive-page' + str(page_number) + '.html'

        if page_number is not 809:
            yield scrapy.Request(new_url, callback=self.parse, meta={'page_number': page_number})

            print("\n\n%d", new_url)



    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//*[@id="col3_content"]/div[2]/div/span/text()').re(r'\d\d-\d\d-\d\d\d\d')),
            'date': ''.join(response.xpath('//*[@id="col3_content"]/div[2]/div/span/text()').re(r'\d\d:\d\d')),
            'title': ''.join(response.xpath('//*[@id="col3_content"]/div[2]/h1/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="col3_content"]/div[2]/div//text()').extract())
            }
