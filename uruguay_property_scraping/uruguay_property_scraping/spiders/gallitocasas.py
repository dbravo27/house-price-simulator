from itemloaders.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from uruguay_property_scraping import items


class GallitoCrawler(CrawlSpider):
    name = "gallitocasas"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    }

    start_urls = ["https://www.gallito.com.uy/inmuebles/casas/alquiler"]
    allowed_domains = ["gallito.com.uy"]

    rules = (
        Rule(LinkExtractor(allow=r"pag=")),
        Rule(LinkExtractor(allow=r"-inmuebles-"), callback="parse_items"),
    )

    def parse_items(self, response):
        item = ItemLoader(items.UruguayPropertyScrapingItem(), response)
        item.add_value("category", "casa")
        item.add_xpath("barrio", '//*[@id="div_datosOperacion"]/div[3]/p/text()')

        item.add_value("departamento", " ")

        item.add_xpath(
            "bedrooms",
            '//*[@id="div_datosOperacion"]/div[4]/p/text()',
            MapCompose(lambda x: x.split()[0]),
        )
        item.add_xpath(
            "bathrooms",
            '//*[@id="div_datosOperacion"]/div[5]/p/text()',
            MapCompose(lambda x: x.split()[0]),
        )
        item.add_xpath(
            "square_meters",
            '//*[@id="div_datosOperacion"]/div[6]/p/text()',
            MapCompose(lambda x: x.split()[0]),
        )
        item.add_xpath(
            "price",
            '//*[@id="div_datosBasicos"]/div/span[@class="precio"]/text()',
            MapCompose(lambda x: x.split()[1]),
        )
        item.add_xpath(
            "currency",
            '//*[@id="div_datosBasicos"]/div/span[@class="precio"]/text()',
            MapCompose(lambda x: x.split()[0]),
        )
        item.add_value("full_link", response.url)
        h_item = item.load_item()
        house = {key: ", ".join(value) for key, value in h_item.items()}
        yield house
