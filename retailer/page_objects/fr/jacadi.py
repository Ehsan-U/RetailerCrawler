from retailer.page_objects.pages import ProductPage
from web_poet import field



class JacadiProduct(ProductPage):
    """
    Page object for the product page on jacadi.fr
    """

    _product_name = "//h2[contains(@class, 'jac-title-center')]/text()"
    _prod_images = "//figure[contains(@class, 'jac-product-splide')]/@data-src"
    _discounted_price = "//span[@class='jac-product-price-value']/text()"
    _listed_price = "//del[@class='jac-product-price-crossed']/text()"
    _product_desc = "//section[@id='product-description-tab']//text()[not(parent::style or parent::script)]"


    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self) -> str:
        return "Jacadi"

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