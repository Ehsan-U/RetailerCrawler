from retailer.page_objects.pages import ProductPage
from web_poet import field


class GeneraleOptiqueProduct(ProductPage):
    """
    Page object for the product page on generale-optique.com
    """

    _product_name = "//span[@class='breadcrumbs__current-page-text']/text()"
    _brand_name = "//span[@class='product-detail-title__subtitle']/text()"
    _prod_images = "//div[@class='product-image-gallery__images']//img/@src"
    _discounted_price = "//span[contains(@class, 'price--discount')]/text()"
    _listed_price = "//span[contains(@class, 'price--strikethrough')]/text()"
    _product_desc = "//section[@class='product-detail-description']//text()"

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