import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class BeautySuccessProduct(ProductPage):
    """
    Page object for the product page on beautysuccess.fr
    """

    _product_name = "//h1[@class='page-product-title']/span[contains(@class, 'product')]//text()"
    _brand_name = "//h1[@class='page-product-title']/span[@class='brand-name']/strong/text()"
    _prod_images = "//div[@id='amasty-gallery-container']/following-sibling::script/text()"
    _discounted_price = "//span[contains(@id, 'product-price')]/@data-price-amount" 
    _listed_price = "//span[contains(@id, 'old-price')]/@data-price-amount" 
    _product_desc = "//div[@class='product data items']/div//text()"

    @field
    def product_name(self) -> str:
        return " ".join(self.response.xpath(self._product_name).getall())
    
    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()
    
    @field
    def prod_images(self) -> list:
        images = []
        data = json.loads(self.response.xpath(self._prod_images).get('{}'))
        for img in data.get('[data-role=amasty-gallery]', {}).get('Amasty_Conf/js/amzoomer', {}).get('data'):
            images.append(img.get("full"))
        return images
    
    @field
    def discounted_price(self) -> str:
        return self.response.xpath(self._discounted_price).get()
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).get()
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        return bool(self.response.xpath(self._listed_price).get())