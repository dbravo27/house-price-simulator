# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UruguayPropertyScrapingItem(scrapy.Item):
    category = scrapy.Field()
    barrio = scrapy.Field()
    departamento = scrapy.Field()
    square_meters = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    full_link = scrapy.Field()
