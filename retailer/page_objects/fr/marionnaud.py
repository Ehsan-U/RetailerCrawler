from retailer.page_objects.pages import ProductPage
from web_poet import field


class MarionnaudProduct(ProductPage):
    """
    Page object for the product page on marionnaud.fr.
    """

    _product_name = "//span[@class='productName']/text()"
    _brand_name = "//span[@class='productBrandName']/text()"
    _prod_images = "//div[@class='productImagePrimaryLink']/img/@src"
    _reviews = "//div[@class='product-review']"
    _review_stars = ".//div[@class='star-rating__filled-stars']/@style"
    _review_text = ".//div[@class='product-review__comment']/text()"
    _discounted_price = "//div[@class='finalPrice']/text()"
    _listed_price = "//div[@class='markdownPrice priceformat' and sup]/text()"
    _product_desc = "(//p[@class='prodInfoTxtData'])[1]//text()"

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
    def reviews(self) -> list:
        reviews = []
        for review in self.response.xpath(self._reviews):
            stars = review.xpath(self._review_stars).re_first("[\d.]+")
            value = review.xpath(self._review_text).get()
            if value:
                reviews.append({
                    "review": value.strip(),
                    "stars": round(int(stars)/20) if stars else 5
                })
        return reviews

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
