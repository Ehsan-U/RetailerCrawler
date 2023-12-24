from retailer.page_objects.pages import ProductPage
from web_poet import field



class IRunProduct(ProductPage):
    """
    Page object for the product page on i-run.fr.
    """

    _product_name = "//div[@id='bc_titre']/h1/text()[2]"
    _brand_name = "//div[@id='bc_titre']/h1/text()[1]"
    _prod_images = "//img[@id='img_principale']/@src"
    _reviews = "//div[@id='bc_comment_global']/div[@class='bc_comment']"
    _review_stars = ".//span[@class='bc_mark_star']/text()"
    _review_text = ".//div[@class='bc_comment_content_body']/text()"
    _discounted_price = "//span[@itemprop='price']/text()"
    _listed_price = "//div[@class='reduc']/span[@class='prixbarre']/text()"
    _product_desc = "//div[@id='bc_avis-irun']//text()[not(parent::style or parent::script)]"


    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()
    
    @field
    def brand_name(self) -> str:
        return self.response.xpath(self._brand_name).get()

    @field
    def prod_images(self) -> list:
        images = set()
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                images.add(str(self.response.urljoin(img)))
                if len(images) == 3:
                    break
        return list(images)
    
    @field
    def reviews(self) -> list:
        reviews = []
        for review in self.response.xpath(self._reviews):
            stars = review.xpath(self._review_stars).get('0')
            value = review.xpath(self._review_text).get()
            if value and '5/5' in stars:
                reviews.append({
                    "review": value.strip(),
                    "stars": 5
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
