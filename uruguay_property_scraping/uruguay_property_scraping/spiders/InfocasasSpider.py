import json
from urllib.parse import urljoin

import scrapy

# base URL
base_url = "https://www.infocasas.com.uy/"


class InfocasasSpider(scrapy.Spider):
    name = "Infocasas"
    allowed_domains = ["infocasas.com.uy"]
    start_urls = [
        "https://www.infocasas.com.uy/alquiler/casas",
        "https://www.infocasas.com.uy/alquiler/apartamentos",
    ]

    def __init__(self, *args, **kwargs):
        super(InfocasasSpider, self).__init__(*args, **kwargs)
        self.items = []

    def parse(self, response):
        listings_wrapper = response.css("section.listingsWrapper")

        for i in range(1, len(listings_wrapper.css("a.lc-cardCover")) + 1):
            last_segment = response.url.split("/")[-1]

            if last_segment.startswith("pagina"):
                category = response.url.split("/")[-2]
            else:
                category = last_segment
            barrio = listings_wrapper.css(
                f"div:nth-child({i}) strong.lc-location::text"
            ).getall()[0]
            departamento = listings_wrapper.css(
                f"div:nth-child({i}) strong.lc-location::text"
            ).getall()[2]

            if (
                len(
                    listings_wrapper.css(
                        f"div:nth-child({i}) div.lc-typologyTag strong::text"
                    ).getall()
                )
                < 6
            ):
                continue

            square_meters = listings_wrapper.css(
                f"div:nth-child({i}) div.lc-typologyTag strong::text"
            ).getall()[5]
            bedrooms = (
                listings_wrapper.css(
                    f"div:nth-child({i}) div.lc-typologyTag strong::text"
                )
                .getall()[0]
                .split(" ")[0]
            )
            bathrooms = listings_wrapper.css(
                f"div:nth-child({i}) div.lc-typologyTag strong::text"
            ).getall()[2]

            price_list = listings_wrapper.css(
                f"div:nth-child({i}) div.lc-price strong::text"
            ).getall()
            if len(price_list) < 4:
                continue

            price = int(price_list[3])
            currency = listings_wrapper.css(
                f"div:nth-child({i}) div.lc-price strong::text"
            ).getall()[1]
            partial_link = listings_wrapper.css(
                f"div:nth-child({i}) a.lc-data ::attr(href)"
            ).get()
            full_link = urljoin(base_url, partial_link)

            self.items.append(
                {
                    "category": category,
                    "barrio": barrio,
                    "departamento": departamento,
                    "square_meters": square_meters,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "price": price,
                    "currency": currency,
                    "full_link": full_link,
                }
            )

        # follow the pagination link if available
        next_page = response.css(
            'a.ant-pagination-item-link[rel="next"]::attr(href)'
        ).get()
        if next_page:
            full_url = urljoin(base_url, next_page)
            yield response.follow(full_url, callback=self.parse)

    def closed(self, reason):
        with open("infocasas.json", "w") as f:
            json.dump(self.items, f)
