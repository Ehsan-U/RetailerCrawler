from enum import Enum
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response
from typing import Dict
from urllib.parse import urlparse

from retailer.utils import build_paginated_url
from retailer.items import RetailerItem
from retailer.page_objects.pages import ProductPage
from retailer.settings import SCRAPY_XPATHS_RULES



################################
#            Spider 1          #
################################

class RetailerSpider(scrapy.Spider):
    """
    Spider for scraping data from the i-run.fr website.
    """
    name = "retailer_spider"
    PAGE_NO = 1


    def start_requests(self):
        """
        Method to generate initial requests for scraping.

        Returns:
            generator: A generator of scrapy.Request objects.
        """
        pages = [
            # {
            #     "url": "https://www.i-run.fr/chaussures_homme/?sorter=&st=&m=&t=&s=b&c=&cat=23&ter=&u=&pc=&pmn=&pmx=&dmn=&dmx=&pxmn=&pxmx=&d=#bc_filtres",
            #     "user_id": 1,
            #     "country_id": 1,
            #     "retailer_id": 1,
            # },
            # {
            #     "url": "https://www.bhv.fr/c/mode-femme-vetements-veste+et+manteau/fttr/0+-10+/10+-20+/20+-30+/30+-40+/40+-50+/50+-60+/60+-70+/70+-80+/80+-90+/prix/71-2250",
            #     "user_id": 2,
            #     "country_id": 2,
            #     "retailer_id": 2,
            # }
            {
                "url": "https://www.bhv.fr/p/manteau+long+kuna+bi+matiere+capuche-woolrich/85726596/320",
                "id": 3,
            }
        ]

        for page in pages:
            url = page.get('url')
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"meta": page})


    async def parse(self, response: Response, page: ProductPage, meta: Dict):
        """
        Method to parse the response and extract product URLs.

        Args:
            response (scrapy.http.Response): The response object.
            page (dict): The page information.

        Yields:
            scrapy.Request: A scrapy.Request object for each product URL.
        """

        # presence of id in meta indicate status check call
        if meta.get("id"):
            partial_item = await page.to_item()
            item = {
                **meta,
                "discounted": partial_item.get("discounted_flag")
            }
            yield item

        else:
            # injection of xpaths based on domain
            domain = urlparse(response.url).netloc.lstrip('www.')
            path = SCRAPY_XPATHS_RULES[domain]()
            
            for product in response.xpath(path.PRODUCTS):
                # only discounted products
                if product.xpath(path.DISCOUNTED):
                    url = response.urljoin(product.xpath(path.PRODUCT_URL).get())
                    yield scrapy.Request(url, cb_kwargs={"meta": meta}, callback=self.parse_product)

            # pagination
            if not response.xpath(path.ERROR):
                self.PAGE_NO +=1
                next_page = build_paginated_url(meta['url'], self.PAGE_NO)
                yield scrapy.Request(url=next_page, cb_kwargs={"meta": meta}, callback=self.parse)



    async def parse_product(self, response: Response, page: ProductPage, meta: Dict):
        """
        Method to parse the product details.

        Args:
            response (scrapy.http.Response): The response object.
            page (dict): The page information.

        Yields:
            dict: The scraped product data.
        """
        partial_item = await page.to_item()
        item = {**meta, **partial_item}

        # remove the source page url
        item.pop("url")

        loader = ItemLoader(item=RetailerItem())
        for k, v in item.items():
            # skip the discounted_flag
            if k != 'discounted_flag':
                loader.add_value(k, v)
            
        yield loader.load_item()






# crawler = CrawlerProcess()
# crawler.crawl(IrunSpider)
# crawler.start()