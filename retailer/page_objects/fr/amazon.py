from urllib.parse import urlsplit, urlunsplit
from retailer.page_objects.pages import ProductPage
from web_poet import field
import os



class AmazonProduct(ProductPage):
    """
    Page object for the product page on amazon.fr.
    """

    _product_name = "//span[@id='productTitle']/text()"
    _brand_name = "//a[@id='bylineInfo']/text()"
    _prod_images = "//div[@id='imgTagWrapperId']/img/@src"
    _reviews = "//div[@data-hook='review']"
    _review_stars = ".//i[contains(@data-hook, 'review-star-rating')]/@class"
    _review_text = ".//div[@data-hook='review-collapsed']//text()"
    _discounted_price = "//span[contains(@class, 'priceToPay')]//span[@class='a-price-whole' or @class='a-price-fraction']/text()"
    _listed_price = "//span[@data-a-strike]/span[@class]/text()"
    _product_desc = "//div[@id='productDescription']//text()"

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
                scheme, netloc, path, query, fragment = urlsplit(src)
                filename = os.path.basename(path)
                if "._" in filename:
                    new_filename = filename.split("._")[0] + "._AC_SX522_.jpg"
                    path = os.path.join(os.path.dirname(path), new_filename)
                src = urlunsplit((scheme, netloc, path, query, fragment))
                if not src in images:
                    images.append(src)
                if len(images) == 3:
                    break
        return images
    
    @field
    def reviews(self) -> list:
        reviews = []
        for review in self.response.xpath(self._reviews):
            stars = review.xpath(self._review_stars).re_first("\d")
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
        return ".".join(self.response.xpath(self._discounted_price).getall())
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).get()
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        return bool(self.response.xpath(self._listed_price).get())
