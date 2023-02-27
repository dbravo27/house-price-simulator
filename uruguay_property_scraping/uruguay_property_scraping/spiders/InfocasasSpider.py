import scrapy
import json
from urllib.parse import urljoin

# base URL
base_url = 'https://www.infocasas.com.uy/'

class InfocasasSpider(scrapy.Spider):
    name = 'Infocasas'
    allowed_domains = ['infocasas.com.uy']
    start_urls = ['https://www.infocasas.com.uy/alquiler/casas']

    def __init__(self, *args, **kwargs):
        super(InfocasasSpider, self).__init__(*args, **kwargs)
        self.items = []
        # Extract the category from the start URL
        self.category = self.start_urls[0].split('/')[-1]  
        
        
    def parse(self, response):
        house_listings = response.css('section div div a.lc-data strong::text').getall()
        
        i = 0
        while i*14 + 12 < len(house_listings):
            category = self.category
            location = house_listings[i*14 + 11] + ', ' + house_listings[i*14 + 12]
            square_meters = house_listings[i*14 + 10]
            bedrooms = house_listings[i*14 + 4]
            bathrooms = house_listings[i*14 + 9]
            price = house_listings[i*14 + 3]
            currency = house_listings[i*14 + 1]
        
            self.items.append({
                'category': category,
                'location': location,
                'square_meters': square_meters,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'price': price,
                'currency': currency
            })

            i += 1
        # follow the pagination link if available
        next_page = response.css('a.ant-pagination-item-link[rel="next"]::attr(href)').get()
        if next_page:
            full_url = urljoin(base_url, next_page)
            yield response.follow(full_url, callback=self.parse)

    def parse_house(self, response):
        self.logger.info('Hi, this is a house page! %s', response.url)
        category = response.css('h1.ant-typography.property-title::text').extract_first().split(" - ")[0]
        location = response.css('div.ant-col.ant-col-24.address span span::text').get()
        square_meters = response.css('div.ant-space-item span.ant-typography::text').extract()[5]
        bedrooms = response.css('div.ant-space-item span.ant-typography::text').get().split(' ')[0]
        bathrooms = response.css('div.ant-space-item span.ant-typography::text').extract()[2]
        price = response.css('span.ant-typography.price strong::text').get().split(' ')[1]
        currency = response.css('span.ant-typography.price strong::text').get().split(' ')[0]

        yield {
            'category': category,
            'location': location,
            'square_meters': square_meters,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'price': price,
            'currency': currency
        }

    def closed(self, reason):
        with open('infocasas.json', 'w') as f:
            json.dump(self.items, f)




