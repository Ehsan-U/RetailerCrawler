import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class FnacProduct(ProductPage):
    """
    Page object for the product page on fnac.com
    """

    _product_name = "//h1[@class='f-productHeader-Title']/text()"
    _brand_name = "//script[@data-automation-id='seo-structured-data']/text()"
    _prod_images = "//img[@class='f-productMedias__viewItem--main']/@src"
    _discounted_price = "//span[@class='f-faPriceBox__price userPrice checked']/text()"
    _listed_price = "//strong[@class='f-faPriceBox__price--striked']/text()"
    _product_desc = "//div[@class='f-productDesc']//text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()
    
    @field
    def brand_name(self) -> str:
        data = json.loads(self.response.xpath(self._brand_name).get('{}'))
        return data.get("brand", {}).get("name")
    
    @field
    def prod_images(self) -> list:
        images = []
        data = json.loads(self.response.xpath(self._brand_name).get('{}'))
        imgs = data.get("image", [])
        for img in imgs:
            if img not in images:
                images.append(img)
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