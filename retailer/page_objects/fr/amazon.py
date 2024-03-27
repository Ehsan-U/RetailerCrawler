from retailer.page_objects.pages import ProductPage
from web_poet import field
import json
from urllib.parse import urlencode, urlsplit, urlunsplit


class AmazonProduct(ProductPage):
    """
    Page object for the product page on amazon.fr.
    """

    _product_name = "//span[@id='productTitle']/text()"
    _brand_name = "//a[@id='bylineInfo']/text()"
    _prod_images = "//div[@id='imgTagWrapperId']//img"
    _reviews = "//div[@data-hook='review']"
    _review_stars = ".//i[contains(@data-hook, 'review-star-rating')]/@class"
    _review_text = ".//div[@data-hook='review-collapsed']//text()"
    _discounted_price = "//div[@id='centerCol']//span[contains(@class, 'priceToPay')]//span[@class='a-price-whole' or @class='a-price-fraction']/text()"
    _listed_price = "//div[@id='centerCol']//span[@data-a-strike]/span[@class]/text()"
    _product_desc = "//div[@id='productDescription']//text()"

    @field
    def product_url(self) -> str:
        scheme, netloc, path, query, fragment = urlsplit(str(self.response.url))
        query = urlencode({"psc": "1"}) # for DB
        if 'ref=' in path:
            path = path.split("ref=")[0]
        url = urlunsplit((scheme, netloc, path, query, fragment))
        return url

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

        found_imgs = self.response.xpath(self._prod_images)
        for img in found_imgs:
            sizes = json.loads(img.xpath("./@data-a-dynamic-image").get("{}"))
            largest_img, largest_img_dimensions = None, None

            for img_url, dimensions in sizes.items():
                width, height = dimensions
                if (largest_img_dimensions is None) or (width * height > largest_img_dimensions[0] * largest_img_dimensions[1]):
                    largest_img = img_url
                    largest_img_dimensions = (width, height)

            if largest_img and not largest_img in images:
                images.append(largest_img)

            if len(images) == 0:
                images.append(img.xpath("./@data-a-hires").get())
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
        return ".".join(self.response.xpath(self._discounted_price).getall()[:2])
    
    @field
    def listed_price(self) -> str:
        return self.response.xpath(self._listed_price).get()
    
    @field
    def product_desc(self) -> str:
        return " ".join(self.response.xpath(self._product_desc).getall())
    
    @field
    def discounted_flag(self) -> bool:
        if self.discounted_percent and self.discounted_percent > 0:
            return True
        else:
            return False