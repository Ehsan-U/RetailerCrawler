from retailer.page_objects.pages import ProductPage
from web_poet import field


class FarfetchProduct(ProductPage):
    """
    Page object for the product page on farfetch.com.
    """

    _product_name = "//p[@data-testid='product-short-description']/text()"
    _brand_name = "//a[@data-component='LinkGhostDark']/text()"
    _prod_image = "//img[contains(@alt, 'Image')]/@src"
    _discounted_price = "//p[@data-component='PriceFinalLarge']/text()"
    _listed_price = "//p[@data-component='PriceOriginal']/text()"
    _product_desc = "//section[@data-component='AccordionItem']//text()[not(parent::style or parent::script)]"


    @field
    def product_name(self):
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self):
        return self.response.xpath(self._brand_name).get()

    @field
    def prod_image(self):
        img = self.response.xpath(self._prod_image).get()
        if img:
            return str(self.response.urljoin(img))
        return img

    @field
    def discounted_price(self):
        return self.response.xpath(self._discounted_price).get()

    @field
    def listed_price(self):
        return self.response.xpath(self._listed_price).get()

    @field
    def product_desc(self):
        return " ".join(self.response.xpath(self._product_desc).getall())

    @field
    def discounted_flag(self):
        return bool(self.response.xpath(self._listed_price).get())