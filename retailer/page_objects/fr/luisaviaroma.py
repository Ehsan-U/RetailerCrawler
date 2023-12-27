from retailer.page_objects.pages import ProductPage
from web_poet import field



class LuisaViaRomaProduct(ProductPage):
    """
    Page object for the product page on luisaviaroma.com.
    """


    _product_name = "//p[@data-id='ItemPage-Description']/text()"
    _brand_name = "//a[@data-id='ItemPage-Designer']/text()"
    _prod_images = "//img[@itemprop='image']/@src"
    _discounted_price = "//div[count(strong)=3]/strong[3]/text()"
    _listed_price = "//div[count(strong)=3]/strong[1]/text()"
    _product_desc = "//span[text()='Details']/parent::h2/parent::div/ul/li//text()"


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