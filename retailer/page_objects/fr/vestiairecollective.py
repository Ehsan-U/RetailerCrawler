from retailer.page_objects.pages import ProductPage
from web_poet import field



class VestiaireCollectiveProduct(ProductPage):
    """
    Page object for the product page on fr.vestiairecollective.com
    """

    _product_name = "//div[@data-cy='productTitle_name']/text()"
    _brand_name = "//div[@data-cy='productTitle_brand']/a/text()"
    _prod_images = "//div[contains(@class, 'images_imageContainer')]/img/@srcset"
    _discounted_price = "//span[contains(@class, 'price--promo')]/text()"
    _listed_price = "//span[contains(@class, 'price--strikeOut')]/text()"
    _product_desc = "//section[contains(@class, 'productPage__moreDetails')]//text()[not(parent::style or parent::script)]"

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
                src = img.split("768w,")[0].split("480w,")[-1].strip().replace("w=128", "w=768").replace("q=75", "q=70")
                src = str(self.response.urljoin(src))
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