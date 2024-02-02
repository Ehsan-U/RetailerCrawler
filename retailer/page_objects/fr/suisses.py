from retailer.page_objects.pages import ProductPage
from web_poet import field


class SuissesProduct(ProductPage):
    """
    Page object for the product page on 3suisses.fr
    """

    _product_name = "//meta[@property='og:title']/@content"
    _brand_name = "//p[@class='brand']/text()"
    _prod_images = "//ul[@id='gallery-3su']//a[@data-url]/img/@src"
    _discounted_price = "//span[@class='dyn_prod_price product__price--new']/text()"
    _listed_price = "//span[@class='dyn_prod_striked_price product__price--old']/text()"
    _product_desc = "//div[@id='product-new-desc']//text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get('').replace(" | 3 SUISSES",'')

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