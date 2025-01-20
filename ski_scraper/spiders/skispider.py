import scrapy
import uuid


class SkispiderSpider(scrapy.Spider):
    name = "skispider"
    allowed_domains = ["skiresort.info"]
    start_urls = ["https://www.skiresort.info/ski-resorts/europe/"]

    def parse(self, response):
        resorts = response.css('div.resort-list-item')

        for resort in resorts:
            name = resort.css('div.h3 a::text').get()
            country = resort.css('div.sub-breadcrumb a:nth-of-type(2)::text').get()
            relative_url = resort.css('div.h3 a::attr(href)').get()

            if relative_url:
                unique_id = str(uuid.uuid4())
                next_page_url = relative_url
                yield response.follow(next_page_url, callback=self.parse_resort_page, meta={'resort_id': unique_id, 'name': name, 'country': country})

        next_page = response.css('ul.pagination li.active + li a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_resort_page(self, response):
        name = response.meta['name']
        country = response.meta['country']
        resort_id = response.meta['resort_id']

        slopes_table = response.css('table.run-table tr')
        price_table = response.css('table.detail-table tr')
        slope = response.css('strong#selSlopetot::text').get()
        desc = response.css('p#selText span.js-more-text::text').get()
        description = desc if desc else response.css('p#selText::text').get()

        # Extract images
        images = response.css('a.js-image-gallery img::attr(src)').getall()

        yield {
            'id': resort_id,
            'name': name,
            'country': country,
            'description': description,
            'elevation': response.css('div.detail-links div#selAlti::text').getall(),
            'slopes': {
                'easy-slope': slopes_table[0].css('.distance::text').get(),
                'intermediate-slope': slopes_table[1].css('.distance::text').get(),
                'difficult-slope': slopes_table[2].css('.distance::text').get(),
            },
            'ski-lift': response.css('div.lift-info-group strong#selLiftstot::text').get(),
            'prices': {
                'adult-price': price_table.css('td#selTicketA::text').get(),
                'youth-price': price_table.css('td#selTicketY::text').get()
            },
            'review': response.css("div.rating-list.js-star-ranking::attr(data-rank)").get(),
            'images': images
        }
