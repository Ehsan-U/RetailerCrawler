# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from price_parser import Price
from itemloaders.processors import Join, MapCompose, TakeFirst



# custom output processor instead of TakeFirst to handle lists
class CustomTakeFirst(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None and value != "":
                return value
        return ""


def clean_str(value: str) -> str:
    """
    Cleans a string by stripping whitespace and other potential unwanted characters.

    Args:
        value: The string to clean.

    Returns:
        The cleaned string.
    """
    if isinstance(value, str):
        value = re.sub(r'\s+', ' ', value)
        return value.replace('\n','').strip()

    return value


def clean_price(value: str) -> float:
    """
    Cleans a price string by stripping whitespace and other potential unwanted characters.

    Args:
        value: The price string to clean.

    Returns:
        The cleaned price string.
    """
    if isinstance(value, str):
        value = Price.fromstring(value).amount_float
        return value

    return value


class RetailerItem(scrapy.Item):
    """
    Represents an item scraped from a retailer's website.

    Attributes:
        user_id (scrapy.Field): The user ID associated with the item.
        country_id (scrapy.Field): The country ID associated with the item.
        retailer_id (scrapy.Field): The retailer ID associated with the item.
        category_ids (scrapy.Field): The category IDs associated with the item.
        product_url (scrapy.Field): The URL of the product.
        product_name (scrapy.Field): The name of the product.
        brand_name (scrapy.Field): The brand name of the product.
        prod_images (scrapy.Field): The images of the product.
        reviews (scrapy.Field): The reviews of the product.
        discounted_price (scrapy.Field): The discounted price of the product.
        listed_price (scrapy.Field): The listed price of the product.
        product_desc (scrapy.Field): The description of the product.
        discounted_flag (scrapy.Field): The discounted flag of the product.
    """

    user_id = scrapy.Field(
        output_processor=CustomTakeFirst()
    )
    country_id = scrapy.Field(
        output_processor=CustomTakeFirst()
    )
    retailer_id = scrapy.Field(
        output_processor=CustomTakeFirst()
    )
    category_ids = scrapy.Field()
    product_url = scrapy.Field(
        output_processor=CustomTakeFirst()
    )
    product_name = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=CustomTakeFirst()
    )
    brand_name = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=CustomTakeFirst()
    )
    prod_images = scrapy.Field()
    reviews = scrapy.Field()
    discounted_price=scrapy.Field(
        input_processor=MapCompose(clean_str, clean_price),
        output_processor=CustomTakeFirst()
    )
    listed_price=scrapy.Field(
        input_processor=MapCompose(clean_str, clean_price),
        output_processor=CustomTakeFirst()
    )
    discounted_percent=scrapy.Field(
        output_processor=CustomTakeFirst()
    )
    product_desc = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=CustomTakeFirst()
    )

    discounted_flag = scrapy.Field(
        output_processor=CustomTakeFirst()
    )

