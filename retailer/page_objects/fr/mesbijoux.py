from retailer.page_objects.pages import ProductPage
from web_poet import field


class MesBijouxProduct(ProductPage):
    """
    Page object for the product page on mes-bijoux.fr
    """

    _product_name = "//meta[@itemprop='name']/@content"
    _brand_name = ""
    _prod_images = "//meta[@itemprop='image']/@content"
    _discounted_price = "//meta[@itemprop='price']/@content"
    _listed_price = "//meta[@property='product:price:amount']/@content"
    _product_desc = "//meta[@itemprop='description']/@content"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self) -> str:
        return "Mes-bijoux"

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
        discounted = (self.response.xpath(self._listed_price).get() != self.response.xpath(self._discounted_price).get())
        return discounted