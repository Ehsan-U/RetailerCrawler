import json
from retailer.page_objects.pages import ProductPage
from web_poet import field


class ParfumsMoinsChersProduct(ProductPage):
    """
    Page object for the product page on parfumsmoinschers.com
    """

    _product_name = "//h1/span[not(@class)]/text()"
    _brand_name = ""
    _prod_images = "//div[@class='productImages ']/img/@src"
    _discounted_price = "//span[@class='productBoxPrice']/text()"
    _listed_price = "//span[@class='productBoxMsrp']/text()"
    _product_desc = "//div[@class='row rowDescription']//text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self) -> str:
        json_str = self.response.xpath("//script[@type='application/ld+json']/text()").get()
        data = json.loads(json_str) if json_str else {}
        return data.get("brand", {}).get("name")

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
        json_str = self.response.xpath("//script[@type='application/ld+json']/text()").get()
        data = json.loads(json_str) if json_str else {}
        return data.get("description", "")

    @field
    def discounted_flag(self) -> bool:
        return self.discounted_percent > 1