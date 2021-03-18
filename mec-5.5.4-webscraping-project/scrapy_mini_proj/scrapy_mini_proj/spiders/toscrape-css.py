import scrapy

class QuotesCSS(scrapy.Spider):
    name = "scrapy_css"

    allowed_data_sets = ['quotes', 'authors']
    data_set = 'quotes' # options: `quotes` or `authors`

    def start_requests(self):
        url = 'http://quotes.toscrape.com'
        
        data_set_arg = getattr(self, 'data_set', None)
        if data_set_arg is not None and data_set_arg in self.allowed_data_sets:
            self.data_set = data_set_arg

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            if self.data_set == 'quotes':
                text = quote.css('span.text::text').get()
                author = quote.css('small.author::text').get()
                tags = quote.css('div.tags a.tag::text').getall()
                yield {
                    'text': text,
                    'author': author,
                    'tags': tags
                }
            if self.data_set == 'authors':
                author_page_links = response.css('.author + a')
                yield from response.follow_all(author_page_links, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }