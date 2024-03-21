import json
from retailer.page_objects.pages import ProductPage
from web_poet import field



class CarrefourProduct(ProductPage):
    """
    Page object for the product page on carrefour.fr
    """

    _product_name = "//div[@id='product-title-desktop']/h1/text()"
    _brand_name = "//script[@type='application/ld+json'][last()]/text()"
    _prod_images = "//div[@data-testid='zoomable-image']/img/@src"
    _discounted_price = "//div[@data-testid='product-price__amount--main']/span[1]/text()"
    _listed_price = "//div[@class='product-price__amount product-price__amount--old']/span[1]/text()"
    _product_desc = "//div[@id='product-characteristics']//text()"

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
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                src = str(self.response.urljoin(img))
                if src not in images:
                    images.append(src)
                if len(images) == 3:
                    break
        if len(images) > 1:
            images[0], images[1] = images[1], images[0]
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