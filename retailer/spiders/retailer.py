from base64 import b64decode

import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response, Request
from typing import Dict, Union, Callable
from urllib.parse import urlparse

from retailer.utils import build_paginated_url
from retailer.items import RetailerItem
from retailer.page_objects.pages import ProductPage
from retailer.products import Products




class RetailerSpider(scrapy.Spider):
    """
    Spider class for scraping retailer websites.
    """

    name = "retailer_spider"
    PAGE_NO = 1
    scrappingtype = 'scrapping'


    def start_requests(self) -> Request:
        """
        Generates initial requests to start scraping.

        Returns:
            Request: The initial request to be processed.
        """
        products = Products();
        pages = products.get_urls(self.scrappingtype)

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
                    js = self.use_javascript(url, page_meta.get("retailer_id"), product_page=True)

                    request = self.make_request(url, callback=self.parse_product, cb_kwargs={"page_meta": page_meta}, js=js)
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
        # allow only discounted products
        if item.get("discounted_percent"):

            # remove the source page url
            item.pop("url")

            loader = ItemLoader(item=RetailerItem())
            for k, v in item.items():
                # skip the discounted_flag
                if k != 'discounted_flag':
                    loader.add_value(k, v)

            yield loader.load_item()
        else:
            pass


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


    def make_request(self, url: str, callback: Callable, cb_kwargs: Dict, js: bool = False, headers: Dict = None) -> Request:
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

        if "intersport.fr" in domain:
            headers = {"Referer": "https://www.intersport.fr/"}
            meta["zyte_api_automap"].update(
                {
                    "httpResponseBody": True,
                    "device": "mobile",
                 }
            )
        
        if 'farfetch.com' in domain:
            headers = {"Accept-Language": "fr-FR"}

        if js:
            meta["zyte_api_automap"].update(
                {'browserHtml': True, 'javascript': True}
            )

            if "fr.vestiairecollective.com" in domain:
                meta["zyte_api_automap"]["actions"] = [
                    # {"action": "waitForTimeout", "timeout": 5},
                    {"action": "waitForSelector", "selector": {"type": "xpath", "value": "//button[@title='Accepter']"}, "timeout": 10},
                    {"action": "click", "selector": {"type": "xpath", "value": "//button[@title='Accepter']"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]

            elif "sunglasshut.com" in domain:
                meta["zyte_api_automap"]["actions"] = [
                    {"action": "waitForSelector", "selector": {"type": "xpath", "value": "//div[@class='geo-buttons']/button"}, "timeout": 10},
                    {"action": "click", "selector": {"type": "xpath", "value": "//div[@class='geo-buttons']/button"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]

        request = scrapy.Request(url, callback=callback, cb_kwargs=cb_kwargs, meta=meta, headers=headers)
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
        
        elif ('placedestendances.com' in domain) or ("jacadi.fr" in domain): 
            if int(element.get()) == self.PAGE_NO: # reached end when PAGE_NO equals the value of the element
                return True
            return False

        if element:
            return True
        return False


    @staticmethod
    def use_javascript(url: str, retailer_id: int, product_page: bool = False) -> bool:
        """
        Determines whether JavaScript should be used for a given URL and retailer ID.

        Args:
            url (str): The URL to check.
            retailer_id (int): The ID of the retailer.
            product_page (bool): Indicates whether the URL is a product page URL. Defaults to False.

        Returns:
            bool: True if JavaScript should be used, False otherwise.
        """
        domain = urlparse(url).netloc.lstrip('www.')

        if ('fr.vestiairecollective.com' in domain) and retailer_id:
            # use javascript only for products listing page
            javascript = True if not product_page else False

        elif ("sunglasshut.com" in domain) and retailer_id:
            # always use javascript for sunglasshut
            javascript = True

        else:
            javascript = False

        return javascript


    @staticmethod
    def save_screenshot(response):
        """
        Saves a screenshot of the page.

        Args:
            response (Response): The response object of the page.
        """
        screenshot: bytes = b64decode(response.raw_api_response["screenshot"])
        with open("screenshot.png", "wb") as f:
            f.write(screenshot)