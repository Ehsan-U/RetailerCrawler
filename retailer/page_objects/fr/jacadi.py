from retailer.page_objects.pages import ProductPage
from web_poet import field



class JacadiProduct(ProductPage):
    """
    Page object for the product page on jacadi.fr
    """

    _product_name = "//h2[contains(@class, 'jac-title-center')]/text()"
    _prod_image = "//figure[contains(@class, 'jac-product-splide')]/@data-src"
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