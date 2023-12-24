from web_poet.pages import WebPage
from web_poet import field

from retailer.utils import calculate_discount



class ProductPage(WebPage):
    
    @field
    def product_url(self) -> str:
        return str(self.response.url)
    
    @field
    def product_name(self) -> str:
        return ''
    
    @field
    def brand_name(self) -> str:
        return ''
    
    @field
    def prod_images(self) -> list:
        return ['']
    
    @field
    def reviews(self) -> list:
        return [{}]
    
    @field
    def discounted_price(self) -> str:
        return ''

    @field
    def listed_price(self) -> str:
        return ''
    
    @field
    def discounted_percent(self) -> float:
        return calculate_discount(self.discounted_price, self.listed_price)
    
    @field
    def product_desc(self) -> str:
        return ''

    # for checking the status of the product
    @field
    def discounted_flag(self) -> bool:
        return None