import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response, Request
from typing import Dict, Union
from urllib.parse import urlparse

from retailer.utils import build_paginated_url
from retailer.items import RetailerItem
from retailer.page_objects.pages import ProductPage
from retailer.settings import SCRAPY_XPATHS_RULES




class RetailerSpider(scrapy.Spider):
    """
    Spider class for scraping retailer websites.
    """

    name = "retailer_spider"
    PAGE_NO = 1


    def start_requests(self) -> Request:
        """
        Generates initial requests to start scraping.

        Returns:
            Request: The initial request to be processed.
        """
        pages = [
            {
                "url": "https://fr.delsey.com/collections/valises-cabine",
                "user_id": 1,
                "country_id": 1,
                "retailer_id": 1,
            }
        ]

        for page in pages:
            url = page.get('url')
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"meta": page})


    async def parse(self, response: Response, page: ProductPage, meta: Dict) -> Union[Request, Dict]:
        """
        Parses the response from the initial request or subsequent requests.

        Args:
            response (Response): The response object.
            page (ProductPage): The product page object.
            meta (Dict): The metadata associated with the request.

        Returns:
            Union[Request, Dict]: The next request to be processed or the scraped item.
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
            if not response.xpath(path.LAST_PAGE):
                self.PAGE_NO += 1
                next_page = build_paginated_url(meta['url'], self.PAGE_NO)
                yield scrapy.Request(url=next_page, cb_kwargs={"meta": meta}, callback=self.parse)


    async def parse_product(self, response: Response, page: ProductPage, meta: Dict) -> RetailerItem:
        """
        Parses the response from the product page request.

        Args:
            response (Response): The response object.
            page (ProductPage): The product page object.
            meta (Dict): The metadata associated with the request.

        Returns:
            RetailerItem: The scraped item.
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