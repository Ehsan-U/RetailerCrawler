# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from price_parser import Price
from itemloaders.processors import Join, MapCompose, TakeFirst



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
        product_url (scrapy.Field): The URL of the product.
        product_name (scrapy.Field): The name of the product.
        brand_name (scrapy.Field): The brand name of the product.
        prod_image (scrapy.Field): The image of the product.
        reviews (scrapy.Field): The reviews of the product.
        discounted_price (scrapy.Field): The discounted price of the product.
        listed_price (scrapy.Field): The listed price of the product.
        product_desc (scrapy.Field): The description of the product.
    """

    user_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    country_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    retailer_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    product_name = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=TakeFirst()
    )
    brand_name = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=TakeFirst()
    )
    prod_image = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=TakeFirst()
    )
    reviews = scrapy.Field()
    discounted_price=scrapy.Field(
        input_processor=MapCompose(clean_str, clean_price),
        output_processor=TakeFirst()
    )
    listed_price=scrapy.Field(
        input_processor=MapCompose(clean_str, clean_price),
        output_processor=TakeFirst()
    )
    discounted_percent=scrapy.Field(
        output_processor=TakeFirst()
    )
    product_desc = scrapy.Field(
        input_processor=MapCompose(clean_str),
        output_processor=TakeFirst()
    )

    discounted_flag = scrapy.Field(
        output_processor=TakeFirst()
    )

