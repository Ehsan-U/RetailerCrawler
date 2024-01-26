import re
from retailer.page_objects.pages import ProductPage
from web_poet import field


class ShoesProduct(ProductPage):
    """
    Page object for the product page on shoes.fr
    """

    _product_name = "//span[@itemprop='name']/h1/text()"
    _brand_name = "//div[@itemprop='brand']/@content"
    _prod_images = "//div[@class='productBigView']//img/@src"
    _discounted_price = "//span[@itemprop='price']/@content"
    _listed_price = "//span[@class='product_price_span']/s/text()"
    _product_desc = "//span[@id='products_description']/text()"

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
                src = str(self.response.urljoin(img))
                if not src in images:
                    images.append(src)
                if len(images) == 3:
                    break
        if len(images) == 1:
            images = list(set([re.sub(r'500_[ABC]\.jpg', f"500_{letter}.jpg", images[0]) for letter in ['A','B','C']]))
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