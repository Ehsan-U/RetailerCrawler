from web_poet.pages import WebPage
from web_poet import field

from retailer.utils import calculate_discount



class ProductPage(WebPage):
    
    @field
    def product_url(self):
        return str(self.response.url)
    
    @field
    def product_name(self):
        return ''
    
    @field
    def brand_name(self):
        return ''
    
    @field
    def prod_image(self):
        return ''
    
    @field
    def reviews(self):
        return [{}]
    
    @field
    def discounted_price(self):
        return ''

    @field
    def listed_price(self):
        return ''
    
    @field
    def discounted_percent(self):
        return calculate_discount(self.discounted_price, self.listed_price)
    
    @field
    def product_desc(self):
        return ''

    # for checking the status of the product
    @field
    def discounted_flag(self):
        return None