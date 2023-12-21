from retailer.page_objects.pages import ProductPage
from web_poet import field



class PlaceDestendancesProduct(ProductPage):
    """
    Page object for the product page on placedestendances.com.
    """

    _product_name = "//div[@class='description']/h1/span/text()"
    _brand_name = "//h2[@class='title']/a/text()"
    _prod_image = "//img[@class='fpImg']/@src"
    _discounted_price = "//div[@class='pricing-wrapper']/div[@class='price']/text()"
    _listed_price = "//div[@class='pricing-wrapper']/div[@class='compared-price']/text()"
    _product_desc = "//div[contains(@class, 'item_description')]//text()[not(parent::style or parent::script)]"


    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()

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