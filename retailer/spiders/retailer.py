from base64 import b64decode
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response, Request
from typing import AsyncGenerator, Dict, Iterable, Union, Callable
from urllib.parse import urlparse, urlsplit, urlunsplit

from retailer.utils import build_paginated_url
from retailer.items import RetailerItem
from retailer.page_objects.pages import ProductPage
from retailer.products import Products
from retailer.domain_config import DOMAIN_SETTINGS


class RetailerSpider(scrapy.Spider):
    """
    Spider class for scraping retailer websites.
    """

    name = "retailer"
    PAGE_NO = 1
    SPIDER_TYPE = 'scraper'
    RETAILER_ID = 0


    def start_requests(self) -> Iterable[Request]:
        products = Products()
        pages = []

        if self.RETAILER_ID != 0:
            pages = products.get_pages(self.RETAILER_ID, self.SPIDER_TYPE)

        for page in pages:
            scrapping_url_id = page.get("scrapping_url_id")
            if scrapping_url_id:
                products.update_scrapping_url_scrapped_datetime(scrapping_url_id)
                page.pop("scrapping_url_id")

            url = self.modify_url(url=page['url'], spider_type=page['spider_type'])
            js = self.use_javascript(url, spider_type=page.get("spider_type"))

            request = self.make_request(url, callback=self.parse, cb_kwargs={"page_meta": page}, js=js)
            yield request


    async def parse(self, response: Response, page: ProductPage, page_meta: Dict) -> AsyncGenerator[Union[Request, Dict], None]:
        """
        Parses the response from the initial request or subsequent requests.
        """
        spider_type = page_meta.get("spider_type")
        if spider_type != "scraper":
            page_item = await page.to_item()
            discounted_flag = page_item.get("discounted_flag")
            if discounted_flag:
                item = {
                    **page_meta,
                    "discounted_flag": discounted_flag,
                    "listed_price": page_item.get("listed_price"),
                    "discounted_price": page_item.get("discounted_price"),
                    "discounted_percent": page_item.get("discounted_percent")
                }
            else:
                item = {
                    **page_meta,
                    "discounted_flag": discounted_flag,
                }
            item.pop("url")
            
            loader = ItemLoader(item=RetailerItem())
            for k, v in item.items():
                if (k != 'url'):
                    loader.add_value(k, v)

            yield loader.load_item()
        else:
            domain = urlparse(response.url).netloc.lstrip('www.')
            paths = None
            for site, settings in DOMAIN_SETTINGS.items():
                if site in domain:
                    paths = settings['selectors']
                    break

            if paths is not None:
                for product in response.xpath(paths['PRODUCTS']):
                    # only discounted products
                    if product.xpath(paths['DISCOUNTED']):
                        product_link = response.urljoin(product.xpath(paths['PRODUCT_URL']).get())
                        url = self.modify_url(product_link, spider_type=spider_type, product_page=True)
                        js = self.use_javascript(url, spider_type, product_page=True)

                        request = self.make_request(url, callback=self.parse_product, cb_kwargs={"page_meta": page_meta}, js=js)
                        yield request

                # pagination
                if not self.reached_end(response, paths['ELEMENT']):
                    self.PAGE_NO += 1
                    next_page = build_paginated_url(page_meta['url'], self.PAGE_NO)
                    js = self.use_javascript(next_page, spider_type)

                    request = self.make_request(url=next_page, callback=self.parse, cb_kwargs={"page_meta": page_meta}, js=js)
                    yield request
                else:
                    self.logger.info("\n[+] Reached End\n")
            else:
                self.logger.info("\n[+] Domain not found\n")


    async def parse_product(self, response: Response, page: ProductPage, page_meta: Dict) -> AsyncGenerator[RetailerItem, None]:
        """
        Parses the response from the product page request.
        """
        page_item = await page.to_item()
        item = {**page_meta, **page_item}
        # allow only discounted products
        if item.get("discounted_percent"):
            # remove the unncesessary fields
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
    def modify_url(url: str, spider_type: str, product_page: bool = False) -> str:
        """
        Modifies the URL if needed before making the request.
        """
        domain = urlparse(url).netloc.lstrip('www.')

        if ('sunglasshut.com' in domain) and spider_type == "scraper" and not product_page:
            url = build_paginated_url(url, 0)
        elif ("amazon." in domain):
            if product_page:
                url += "&psc=1" # select the product size to appear discount
        elif ("shoes.fr" in domain or "spartoo.com" in domain):
            url = url.replace("php#","php?")
        elif ("darty.com" in domain):
            scheme, netloc, path, query, fragment = urlsplit(url)
            netloc = "m.darty.com"
            path = path.replace("/nav/", "/m/")
            url = urlunsplit((scheme, netloc, path, query, fragment))
        return url


    def make_request(self, url: str, callback: Callable, cb_kwargs: Dict, js: bool = False, headers: Dict = None) -> Request:
        """
        Creates a scrapy Request object with the given parameters.
        """
        domain = urlparse(url).netloc.lstrip('www.')
        config = DOMAIN_SETTINGS[domain]

        headers = config.get("headers")
        location = self.settings["GEOLOCATIONS"][
            cb_kwargs['page_meta'].get("country_id", 75)
        ]
        meta = {
            "zyte_api_automap": {
                "geolocation": location, 
                **config.get("zyte_extra_args", {})
            }
        }
        if js:
            meta['zyte_api_automap'].update(config['javascript'].get("args", {}))

        request = scrapy.Request(url, callback=callback, cb_kwargs=cb_kwargs, meta=meta, headers=headers)
        return request


    def reached_end(self, response: Response, element_xpath: str) -> bool:
        """
        Checks if the end of the page has been reached.
        """
        domain = urlparse(response.url).netloc.lstrip('www.')
        config = DOMAIN_SETTINGS[domain]
        element = response.xpath(element_xpath)

        # for amazon only
        if 'page_limit' in config:
            if self.PAGE_NO > config['page_limit']:
                return True
        
        if config['end']['condition'] == "element_present":
            if config['end']['negate']:
                result = not bool(element)
            else:
                result = bool(element)

        elif config['end']['condition'] == 'page_no_eq_val':
            if config['end']['negate']:
                result = not (int(element.get()) == self.PAGE_NO) 
            else: 
                result = (int(element.get()) == self.PAGE_NO)

        elif config['end']['condition'] == 'page_no_gt_len':
            if config['end']['negate']: 
                result = not (self.PAGE_NO > len(element.getall())) 
            else:
                result = (self.PAGE_NO > len(element.getall()))

        elif config['end']['condition'] == 'page_no_gt_val':
            if config['end']['negate']:
                result = not (self.PAGE_NO > int(element.get('0'))) 
            else:
                result = (self.PAGE_NO > int(element.get('0')))
        
        return result


    @staticmethod
    def use_javascript(url: str, spider_type: str, product_page: bool = False) -> bool:
        """
        Determines whether JavaScript should be used for a given URL.
        """
        domain = urlparse(url).netloc.lstrip('www.')
        config = DOMAIN_SETTINGS[domain]
        
        if spider_type == "checker":
            product_page = True

        if product_page:
            return config['javascript']['product_page']
        else:
            return config['javascript']['listing_page']  


    @staticmethod
    def save_screenshot(response):
        """
        Saves a screenshot of the page.
        """
        screenshot: bytes = b64decode(response.raw_api_response["screenshot"])
        with open("screenshot.png", "wb") as f:
            f.write(screenshot)

