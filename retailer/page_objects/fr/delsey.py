from retailer.page_objects.pages import ProductPage
from web_poet import field



class DelseyProduct(ProductPage):
    """
    Page object for the product page on fr.delsey.com.
    """

    _product_name = "//h1[@class='h2 product-single__title text-uppercase']/text()"
    _brand_name = "//div[@class='product_single_type text_letter_spacing text-uppercase']/text()"
    _prod_images = "//div[@class='product__main-photos']//img[@class='lazyloaded']/@src"
    _discounted_price = "//span[@class='product__price on-sale']/span[@class]/text()"
    _listed_price = "//span[@class='product__price product__price--compare']/span[@class]/text()"
    _product_desc = "//div[contains(@id, 'Product-content')]//text()[not(parent::style or parent::script)]"

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