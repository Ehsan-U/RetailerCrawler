from retailer.page_objects.pages import ProductPage
from web_poet import field



class BhvProduct(ProductPage):
    """
    Page object for the product page on bhv.fr.
    """

    _product_name = "//p[@class='product-name']/text()"
    _brand_name = "//a[@class='product-brand-text']/text()"
    _prod_image = "//ul[@class='product-display-images']/li/img/@src[1]"
    _discounted_price = "//p[@class='product-price-current']/text()"
    _listed_price = "//p[@class='product-price-old']/text()"
    _product_desc = "//div[@class='product-description']//text()[not(parent::style or parent::script)]"


    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()
    
    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()
    
    @field
    def prod_image(self) -> str:
        img = self.response.xpath(self._prod_image).get()
        if img:
            return str(self.response.urljoin(img))
        return img
    
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