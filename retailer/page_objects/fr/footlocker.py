import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class FootlockerProduct(ProductPage):
    """
    Page object for the product page on footlocker.fr
    """

    _product_name = "//span[@itemprop='name']/text()"
    _brand_name = "//script[@id='productLdJson']/text()"
    _prod_images = "//div[@class='ProductGallery']//img/@src"
    _discounted_price = "//span[@class='ProductPrice-sale']/span[@class='ProductPrice-final']"
    _listed_price = "//span[@class='ProductPrice-sale']/span[@class='ProductPrice-original']/text()"
    _product_desc = "//div[@id='ProductDetails-tabs-details-panel']//text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()
    
    @field
    def brand_name(self) -> str:
        data = json.loads(self.response.xpath(self._brand_name).get('{}'))
        return data.get("brand")
    
    @field
    def prod_images(self) -> list:
        images = []
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                src = str(self.response.urljoin(img))
                if src not in images:
                    images.append(src)
                if len(images) == 3:
                    break
        return images
    
    @field
    def discounted_price(self) -> str:
        return self.response.xpath(self._discounted_price).re_first("\d+\,\d+")
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).re_first("\d+\,\d+")
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        return bool(self.response.xpath(self._listed_price).get())