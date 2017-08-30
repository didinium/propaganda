import scrapy

class AlahedSpider(scrapy.Spider):
    name = 'alahed'
    base_urls = ['http://english.alahednews.com.lb/catessays.php?cid=385', 'http://english.alahednews.com.lb/catessays.php?cid=386', 'http://english.alahednews.com.lb/catessays.php?cid=388', 'http://english.alahednews.com.lb/catessays.php?cid=387', 'http://english.alahednews.com.lb/catessays.php?cid=525', 'http://english.alahednews.com.lb/catessays.php?cid=524', 'http://english.alahednews.com.lb/catessays.php?cid=547', 'http://english.alahednews.com.lb/catessays.php?cid=389', 'http://english.alahednews.com.lb/catessays.php?cid=548', 'http://english.alahednews.com.lb/catessays.php?cid=515', 'http://english.alahednews.com.lb/catessays.php?cid=526', 'http://english.alahednews.com.lb/catessays.php?cid=527', 'http://english.alahednews.com.lb/catessays.php?cid=456', 'http://english.alahednews.com.lb/catessays.php?cid=528', 'http://english.alahednews.com.lb/catessays.php?cid=542', 'http://english.alahednews.com.lb/catessays.php?cid=543', 'http://english.alahednews.com.lb/catessays.php?cid=544', 'http://english.alahednews.com.lb/catessays.php?cid=549', 'http://english.alahednews.com.lb/catessays.php?cid=393', 'http://english.alahednews.com.lb/catessays.php?cid=529', 'http://english.alahednews.com.lb/catessays.php?cid=530', 'http://english.alahednews.com.lb/catessays.php?cid=391', 'http://english.alahednews.com.lb/catessays.php?cid=545', 'http://english.alahednews.com.lb/catessays.php?cid=531', 'http://english.alahednews.com.lb/catessays.php?cid=532', 'http://english.alahednews.com.lb/catessays.php?cid=546', 'http://english.alahednews.com.lb/catessays.php?cid=533', 'http://english.alahednews.com.lb/catessays.php?cid=551', 'http://english.alahednews.com.lb/catessays.php?cid=535', 'http://english.alahednews.com.lb/catessays.php?cid=536', 'http://english.alahednews.com.lb/catessays.php?cid=537', 'http://english.alahednews.com.lb/catessays.php?cid=539', 'http://english.alahednews.com.lb/catessays.php?cid=522', 'http://english.alahednews.com.lb/catessays.php?cid=552']

    def start_requests(self):
        for base_url in self.base_urls:
            yield scrapy.Request(base_url, meta={'page_number': 1, 'base_url': base_url})

    def parse(self, response):
        for article_url in response.xpath('//*[@id="table45"]//@href').extract():
            yield scrapy.Request(response.urljoin(article_url), callback=self.parse_article)

        # for next_article in (response.xpath('//*[@id="mega-menu-5"]/li[2]//@href').extract()):
        #     yield response.follow(next_article, callback=self.parse)

        page_number = response.meta['page_number'] + 1
        base_url = response.meta['base_url']

        if response.xpath('//*[@id="table49"]/tr/td//img/@alt').re(r'Next'):
            new_string = base_url + "&catdd=0&page=" + str(page_number)
            yield scrapy.Request(new_string, callback=self.parse, meta={'page_number': page_number})






    def parse_article(self, response):
        yield {
            'date': ''.join(response.xpath('//*[@id="table36"]//td/p').re(r'> (\d\d-\d\d-\d\d\d\d)')),
            'time': ''.join(response.xpath('//*[@id="table36"]//td/p').re(r'\d\d:\d\d')),
            'title': ''.join(response.xpath('//*[@id="textFontSize1"]/text()').extract_first()),
            'text': ''.join(response.xpath('//*[@id="textFontSize2"]/font[2]/text()').extract()),
        }
