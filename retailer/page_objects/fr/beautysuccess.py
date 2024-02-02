import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class BeautySuccessProduct(ProductPage):
    """
    Page object for the product page on beautysuccess.fr
    """

    _product_name = "//h1[@class='page-product-title']/span[@class='page-title-wrapper product']/span/text()"
    _brand_name = "//h1[@class='page-product-title']/span[@class='brand-name']/strong/text()"
    _prod_images = "//meta[@property='og:image']/@content"
    _discounted_price = "//span[contains(@id, 'product-price')]/@data-price-amount" 
    _listed_price = "//span[contains(@id, 'old-price')]/@data-price-amount" 
    _product_desc = "//div[@class='product data items']//text()"

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