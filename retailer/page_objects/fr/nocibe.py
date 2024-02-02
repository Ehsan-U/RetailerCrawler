import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class NocibeProduct(ProductPage):
    """
    Page object for the product page on nocibe.fr
    """

    _product_name = "//div[@itemprop='name']/text()"
    _brand_name = "//div[@itemprop='brand']/text()"
    _prod_images = "//product-gallery//image-base/@src"
    _discounted_price = "//span[contains(@class, 'prdct__bullets__item__price')]/text() | //div[@itemprop='price']/@content" 
    _listed_price = "//span[@class='striked']/text() | //div[contains(@class, '--strike')]/text()" 
    _product_desc = "//div[@class='prdct__details-wrap']//text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()
    
    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()
    
    @field
    def prod_images(self) -> list:
        images = []
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                src = str(self.response.urljoin(img)).replace("85x85", "1000x1000")
                if not src in images:
                    images.append(src)
                if len(images) == 3:
                    break
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