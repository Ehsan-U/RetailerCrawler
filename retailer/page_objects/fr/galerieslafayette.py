import re
from retailer.page_objects.pages import ProductPage
from web_poet import field



class GalerieslaFayetteProduct(ProductPage):
    """
    Page object for the product page on galerieslafayette.com
    """

    _product_name = "//span[@class='product-title']/text()"
    _brand_name = "//a[@class='store-name']/text()"
    _prod_images = "//ul[@data-js]//img/@src"
    _discounted_price = "//span[@id='current-price']/text()" 
    _listed_price = "//del[@id='old-price']/text()" 
    _product_desc = "//div[contains(@class, 'description tabs-content')]//text()"

    @field
    def product_name(self) -> str:
        return " ".join(self.response.xpath(self._product_name).getall())
    
    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()
    
    @field
    def prod_images(self) -> list:
        images = []
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                src = str(self.response.urljoin(img))
                src = re.sub(r'width=\d+', 'width=616', src)
                src = re.sub(r'height=\d+', 'height=672', src)
                if not src in images:
                    images.append(src)
                if len(images) == 3:
                    break
        return images
    
    @field
    def discounted_price(self) -> str:
        return "".join(self.response.xpath(self._discounted_price).getall())
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).get()
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        return bool(self.response.xpath(self._listed_price).get())