from retailer.page_objects.pages import ProductPage
from web_poet import field


class ManomanoProduct(ProductPage):
    """
    Page object for the product page on manomano.fr
    """

    _product_name = "//h1/text()"
    _brand_name = "//div[@data-testid='carousel-brand']/img/@alt"
    _prod_images = "//img[contains(@src, 'cdn.manomano.com')]/@src"
    _reviews = "//div[@data-testid='Reviews']/div[1]/div"
    _review_stars = ".//span/@aria-label"
    _review_text = ".//div[@style='-webkit-line-clamp:3']/text()"
    _discounted_price = "//div[@data-testid='main-price-exponent']/parent::div//text()"
    _listed_price = "//div[contains(text(), '€') and not(@data-testid='main-price-exponent')]/text()"
    _product_desc = "//div[@data-testid='description-content']/text()"

    @field
    def product_name(self) -> str:
        return self.response.xpath(self._product_name).get()

    @field
    def brand_name(self) -> str:
        brandname = self.response.xpath(self._brand_name).get()
        if brandname:
            brandname = brandname.replace('\u202f', ' ').replace(u'\xa0', ' ').replace(u'\xc2', ' ')
            return brandname.replace('Brand: ', '').replace('Marque : ', '').replace('Visiter la boutique ', '')
        return ''

    @field
    def prod_images(self) -> list:
        images = []
        imgs = self.response.xpath(self._prod_images).getall()
        for img in imgs:
            if img and isinstance(img, str):
                src = str(self.response.urljoin(img))
                if src not in images:
                    images.append(src)
                if len(images) == 3:
                    break
        return images
    
    @field
    def reviews(self) -> list:
        reviews = []
        for review in self.response.xpath(self._reviews):
            stars = review.xpath(self._review_stars).get('').split("/")[0]
            value = " ".join(review.xpath(self._review_text).getall()).strip()
            if value and stars:
                if int(stars) >= 4:
                    reviews.append({
                        "review": value.strip(),
                        "stars": stars
                    })
        return reviews 
    
    @field
    def discounted_price(self) -> str:
        price = ''
        for i in self.response.xpath(self._discounted_price).getall():
            if '€' not in i:
                price += i + '.'
        return price.strip(".")
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).get()
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        return bool(self.response.xpath(self._listed_price).get())
