from enum import Enum
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Response
from typing import Dict

from retailer.items import RetailerItem
from retailer.utils import calculate_discount, build_paginated_url


################################
#            Spider 1          #
################################

class IrunSpider(scrapy.Spider):
    """
    Spider for scraping data from the i-run.fr website.
    """
    name = "irun_spider"
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
        self.reviews_path = Paths.REVIEWS.value
        self.review_stars_path = Paths.REVIEW_STARS.value
        self.review_text_path = Paths.REVIEW_TEXT.value
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
                "url": "https://www.i-run.fr/chaussures_homme/?sorter=&st=&m=&t=&s=b&c=&cat=23&ter=&u=&pc=&pmn=&pmx=&dmn=&dmx=&pxmn=&pxmx=&d=#bc_filtres",
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
            # only discounted products
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

        reviews = []
        for review in response.xpath(self.reviews_path):
            stars = review.xpath(self.review_stars_path).get('0')
            value = review.xpath(self.review_text_path).get()
            if value and '5/5' in stars:
                reviews.append({
                    "review": value.strip(),
                    "stars": 5
                })

        loader.add_value("user_id", page.get("user_id"))
        loader.add_value("country_id", page.get("country_id"))
        loader.add_value("retailer_id", page.get("retailer_id"))
        loader.add_value("product_url", response.url)
        loader.add_value("product_name", response.xpath(self.product_name_path).get())
        loader.add_value("brand_name", response.xpath(self.brand_name_path).get())
        loader.add_value("prod_image", response.xpath(self.product_image_path).get())
        loader.add_value("reviews", reviews if reviews else [{}])
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
        
class IrunSpiderCheck(scrapy.Spider):
    name = "irun_check_spider"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.discount_flag = Paths.DISCOUNTED_FLAG.value


    def start_requests(self):
        products = [
            {
                "url": "https://www.i-run.fr/chaussures_homme/Running_c23/Hoka-One-One_m143/Hoka-One-One-Arahi-6-Wide-M_Hoka-One-One_fiche_115096.html",
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
    
    PRODUCTS = "//section[@class='catalog-page-section']/div"
    DISCOUNTED = ".//span[@class='prixbarre']"
    PRODUCT_URL = "./a/@href"
    ERROR = "//h1[text()='Erreur 404']"
    PRODUCT_NAME = "//div[@id='bc_titre']/h1/text()[1]"
    BRAND_NAME = "//div[@id='bc_titre']/h1/text()[2]"
    PROD_IMAGE = "//img[@id='img_principale']/@src"
    REVIEWS = "//div[@id='bc_comment_global']/div[@class='bc_comment']"
    REVIEW_STARS = ".//span[@class='bc_mark_star']/text()"
    REVIEW_TEXT = ".//div[@class='bc_comment_content_body']/text()"
    DISCOUNTED_PRICE = "//span[@itemprop='price']/text()"
    LISTED_PRICE = "//div[@class='reduc']/span[@class='prixbarre']/text()"
    PRODUCT_DESC = "//div[@id='bc_avis-irun']//text()"

    DISCOUNTED_FLAG = "//span[@class='prixbarre']"

# crawler = CrawlerProcess()
# crawler.crawl(IrunSpider)
# crawler.start()