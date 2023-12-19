from enum import Enum
from typing import Dict
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response

from retailer.items import RetailerItem
from retailer.utils import build_paginated_url, calculate_discount



################################
#            Spider 1          #
################################

class BhvSpider(scrapy.Spider):
    """
    Spider for scraping data from the bhv.fr website.
    """
    name = "bhv_spider"
    PAGE_NO = 1


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.products_path = Paths.PRODUCTS.value
        self.discount_path = Paths.DISCOUNTED.value
        self.product_url_path = Paths.PRODUCT_URL.value
        self.error_path = Paths.ERROR.value
        self.product_name_path = Paths.PRODUCT_NAME.value
        self.brand_name_path = Paths.BRAND_NAME.value
        self.product_image_path = Paths.PROD_IMAGE.value
        self.discount_price_path = Paths.DISCOUNTED_PRICE.value
        self.listed_price_path = Paths.LISTED_PRICE.value
        self.product_desc_path = Paths.PRODUCT_DESC.value


    def start_requests(self):
        """
        Method to generate initial requests for scraping.

        Returns:
            generator: A generator of scrapy.Request objects.
        """
        pages = [
            {
                "url": "https://www.bhv.fr/c/mode-femme-vetements-veste+et+manteau/fttr/0+-10+/10+-20+/20+-30+/30+-40+/40+-50+/50+-60+/60+-70+/70+-80+/80+-90+/prix/71-2250",
                "user_id": 1,
                "country_id": 10,
                "retailer_id": 100
            }
        ]

        for page in pages:
            url = page.get('url')
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"page": page})


    def parse(self, response: Response, page: Dict):
        """
        Method to parse the response and extract product URLs.

        Args:
            response (scrapy.http.Response): The response object.
            page (dict): The page information.

        Yields:
            scrapy.Request: A scrapy.Request object for each product URL.
        """
        for product in response.xpath(self.products_path):
            # filter discounted products
            if product.xpath(self.discount_path):
                url = product.xpath(self.product_url_path).get()
                yield response.follow(url, cb_kwargs={"page": page}, callback=self.parse_product)

        # pagination
        if not response.xpath(Paths.ERROR.value):
            self.PAGE_NO +=1
            next_page = build_paginated_url(page['url'], self.PAGE_NO)
            yield scrapy.Request(url=next_page, cb_kwargs={"page": page}, callback=self.parse)


    def parse_product(self, response: Response, page: Dict):
        """
        Method to parse the product details.

        Args:
            response (scrapy.http.Response): The response object.
            page (dict): The page information.

        Yields:
            dict: The scraped product data.
        """
        loader = ItemLoader(item=RetailerItem(), response=response)

        loader.add_value("user_id", page.get("user_id"))
        loader.add_value("country_id", page.get("country_id"))
        loader.add_value("retailer_id", page.get("retailer_id"))
        loader.add_value("product_url", response.url)
        loader.add_value("product_name", response.xpath(self.product_name_path).get())
        loader.add_value("brand_name", response.xpath(self.brand_name_path).get())
        loader.add_value("prod_image", response.urljoin(response.xpath(self.product_image_path).get('')))
        loader.add_value("reviews", [{}])
        loader.add_value("discounted_price", response.xpath(self.discount_price_path).get())
        loader.add_value("listed_price", response.xpath(self.listed_price_path).get())
        loader.add_value("discounted_percent", 
            calculate_discount(
                loader.get_output_value("discounted_price"), 
                loader.get_output_value("listed_price")
            )
        )
        loader.add_value("product_desc", " ".join(response.xpath(self.product_desc_path).getall()))

        yield loader.load_item()



################################
#            Spider 2          #
################################

class BhvSpiderCheck(scrapy.Spider):
    """
    Spider for checking if a product is discounted on the Bhv website.
    """
    name = "bhv_check_spider"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.discount_flag = Paths.DISCOUNTED_FLAG.value


    def start_requests(self):
        products = [
            {
                "url": "https://www.bhv.fr/p/doudoune+longue+aliquippa+capuche-woolrich/85726606/175",
                "id": 1,
            }
        ]

        for product in products:
            url = product.get('url')
            yield scrapy.Request(url, callback=self.parse, cb_kwargs={"product": product})


    def parse(self, response: Response, product: Dict):
        """
        Check if the product is discounted.
        """
        if response.xpath(self.discount_flag):
            item = {
                **product,
                "discounted": True,
            }
        else:
            item = {
                **product,
                "discounted": False,
            }

        return item



class Paths(Enum):
    """
    Enum for the different xpaths.
    """
    
    PRODUCTS = "//ul[@class='category-products']/li"
    DISCOUNTED = ".//span[contains(@class, 'product-price-old')]"
    PRODUCT_URL = ".//div[contains(@class, 'product-link')]/@data-link"
    ERROR = "//p[@class='category-noresults']"
    PRODUCT_NAME = "//p[@class='product-name']/text()"
    BRAND_NAME = "//a[@class='product-brand-text']/text()"
    PROD_IMAGE = "//ul[@class='product-display-images']/li/img/@src[1]"
    DISCOUNTED_PRICE = "//p[@class='product-price-current']/text()"
    LISTED_PRICE = "//p[@class='product-price-old']/text()"
    PRODUCT_DESC = "//div[@class='product-description']//text()"

    DISCOUNTED_FLAG = "//p[@class='product-price-old']"

# crawler = CrawlerProcess()
# crawler.crawl(IrunSpider)
# crawler.start()