from urllib.parse import urlsplit, urlunsplit
from retailer.page_objects.pages import ProductPage
from web_poet import field



class DartyProduct(ProductPage):
    """
    Page object for the product page on m.darty.com
    """

    _product_name = "//span[@itemprop='name']/text()"
    _brand_name = "//a[@class='product-family']/text()"
    _prod_images = "//div[@data-automation-id='product_main_picture']//img[@class='']/@src"
    _discounted_price = "//div[@class='product-price__price price_ir']/text()"
    _listed_price = "//div[contains(@class, 'product-price__price--is-striped')]/text()"
    _product_desc = "//div[@itemprop='description']//text()"

    @field
    def product_url(self) -> str:
        scheme, netloc, path, query, fragment = urlsplit(self.url)
        netloc = "www.darty.com"
        path = path.replace("/m/", "/nav/")
        url = urlunsplit((scheme, netloc, path, query, fragment))
        return url

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