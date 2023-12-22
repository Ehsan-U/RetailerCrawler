import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response, Request
from typing import Dict, Union, Callable
from urllib.parse import urlparse

from retailer.utils import build_paginated_url
from retailer.items import RetailerItem
from retailer.page_objects.pages import ProductPage




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
                "url": "https://www.sunglasshut.com/fr/balenciaga/6e000232-889652345284",
                "user_id": 1,
                "country_id": 75,
                "retailer_id": 1,
                "category_ids": [1,2]
            }
        ]

        for page in pages:
            url = self.make_url(page)
            js = self.use_javascript(url, page.get("retailer_id"))

            request = self.make_request(url, callback=self.parse, cb_kwargs={"page_meta": page}, js=js)
            yield request


    async def parse(self, response: Response, page: ProductPage, page_meta: Dict) -> Union[Request, Dict]:
        """
        Parses the response from the initial request or subsequent requests.

        Args:
            response (Response): The response object.
            page (ProductPage): The product page object.
            page_meta (Dict): The metadata associated with the request.

        Returns:
            Union[Request, Dict]: The next request to be processed or the scraped item.
        """
        # presence of id in meta indicate status check call
        if page_meta.get("id"):
            partial_item = await page.to_item()
            item = {
                **page_meta,
                "discounted": partial_item.get("discounted_flag")
            }
            yield item
        else:
            domain = urlparse(response.url).netloc.lstrip('www.')
            path = self.settings.get("SCRAPY_XPATHS_RULES").get(domain)

            for product in response.xpath(path.PRODUCTS):
                # only discounted products
                if product.xpath(path.DISCOUNTED):
                    url = response.urljoin(product.xpath(path.PRODUCT_URL).get())

                    request = self.make_request(url, callback=self.parse_product, cb_kwargs={"page_meta": page_meta})
                    yield request

            # pagination
            if not self.reached_end(response, path.ELEMENT):
                self.PAGE_NO += 1
                next_page = build_paginated_url(page_meta['url'], self.PAGE_NO)
                js = self.use_javascript(next_page, page_meta.get("retailer_id"))

                request = self.make_request(url=next_page, callback=self.parse, cb_kwargs={"page_meta": page_meta}, js=js)
                yield request


    async def parse_product(self, response: Response, page: ProductPage, page_meta: Dict) -> RetailerItem:
        """
        Parses the response from the product page request.

        Args:
            response (Response): The response object.
            page (ProductPage): The product page object.
            page_meta (Dict): The metadata associated with the request.

        Returns:
            RetailerItem: The scraped item.
        """
        partial_item = await page.to_item()
        item = {**page_meta, **partial_item}

        # remove the source page url
        item.pop("url")

        loader = ItemLoader(item=RetailerItem())
        for k, v in item.items():
            # skip the discounted_flag
            if k != 'discounted_flag':
                loader.add_value(k, v)

        yield loader.load_item()


    @staticmethod
    def make_url(page_meta: Dict) -> str:
        """
        Get url from page

        Args:
            page_meta (Dict): The data associated with the page

        Returns:
            Modified URL if needed otherwise as it is
        """
        url = page_meta['url']
        domain = urlparse(url).netloc.lstrip('www.')

        if ('sunglasshut.com' in domain) and page_meta.get("retailer_id"):
            url = build_paginated_url(url, 0)

        return url


    def make_request(self, url: str, callback: Callable, cb_kwargs: Dict, js: bool = False) -> Request:
        """
        Creates a scrapy Request object with the given parameters.

        Args:
            url (str): The URL to make the request to.
            callback (Callable): The callback function to be called when the response is received.
            cb_kwargs (Dict): Keyword arguments to be passed to the callback function.
            js (bool, optional): Indicates whether JavaScript should be enabled for the request. Defaults to False.

        Returns:
            Request: The scrapy Request object.
        """
        domain = urlparse(url).netloc.lstrip('www.')
        location = self.settings["GEOLOCATIONS"][
            cb_kwargs['page_meta'].get("country_id", 75)
        ]

        meta = {
            "zyte_api_automap": {
                "geolocation": location,
            }
        }

        if js:
            meta["zyte_api_automap"].update(
                {'browserHtml': True, 'javascript': True}
            )

            if "fr.vestiairecollective.com" in domain:
                meta["zyte_api_automap"]["actions"] = [
                    {"action": "click", "selector": {"type": "xpath", "value": "//button[@title='Accepter']"},},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]

            elif "sunglasshut.com" in domain:
                meta["zyte_api_automap"]["actions"] = [
                    {"action": "click", "selector": {"type": "xpath", "value": "//div[@class='geo-buttons']/button"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]

        request = scrapy.Request(url, callback=callback, cb_kwargs=cb_kwargs, meta=meta)
        return request


    def reached_end(self, response: Response, element_xpath: str) -> bool:
        """
        Checks if the end of the page has been reached.

        Args:
            response (Response): The response object of the page.
            element_xpath (str): The XPath expression to locate the element indicating the end of the page.

        Returns:
            bool: True if the end of the page has been reached, False otherwise.
        """
        domain = urlparse(response.url).netloc.lstrip('www.')
        element = response.xpath(element_xpath)
        
        if ('fr.vestiairecollective.com' in domain):
            if element:
                return False
            return True
        
        elif ('placedestendances.com' in domain): 
            if int(element.get()) == self.PAGE_NO: # reached end when PAGE_NO equals the value of the element
                return True
            return False

        if element:
            return True
        return False


    @staticmethod
    def use_javascript(url: str, retailer_id: int) -> bool:
        """
        Determines whether JavaScript should be used for a given URL and retailer ID.

        Args:
            url (str): The URL to check.
            retailer_id (int): The ID of the retailer.

        Returns:
            bool: True if JavaScript should be used, False otherwise.
        """
        domain = urlparse(url).netloc.lstrip('www.')

        if ('fr.vestiairecollective.com' in domain or "sunglasshut.com" in domain) and retailer_id:
            javascript = True
        else:
            javascript = False

        return javascript
