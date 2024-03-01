import os
import mysql.connector
from dotenv import load_dotenv
from scrapy.exceptions import DropItem
from retailer.product_brand import ProductBrand

class Products:
    db = ""
    cursor = ""

    brand_manager: ProductBrand

    def __init__(self):
        load_dotenv()
        DB_HOST = os.getenv('DB_HOST')
        DB_NAME = os.getenv('DB_NAME')
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_PORT = os.getenv("DB_PORT")

        self.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            use_pure=False
        )
        self.cursor = self.db.cursor()
        self.brand_manager = ProductBrand(self.db)

    def get_pages(self, retailer_id, spider_type):
        if (spider_type == "checker"):
            return self.fetch_existing_products(retailer_id)
        else:
            return self.fetch_scrapping_urls(retailer_id)
        pass

    def fetch_scrapping_urls(self, retailer_id):
        urls = []
        query = f"SELECT su.id, su.user_id, su.country_id, su.url as link, su.retailer_id FROM scrapping_urls AS su LEFT JOIN retailer AS r ON r.id = su.retailer_id WHERE su.status = 'active' AND r.status = 'active' AND r.id = {retailer_id};"
        cursor = self.db.cursor()
        cursor.execute(query)

        for (_id, user_id, country_id, link, retailer_id) in cursor.fetchall():
            url = {}
           
            url['scrapping_url_id'] = _id
            url['user_id'] = user_id
            url['country_id'] = country_id
            url['url'] = link
            url['retailer_id'] = retailer_id
            url['spider_type'] = "scraper"

            query_cat = f"SELECT category_id FROM scrapping_urls_category WHERE scrapping_urls_id = {str(_id)}"
            temp = self.db.cursor()
            temp.execute(query_cat)
            category_ids = temp.fetchall()
            if category_ids:
                url['category_ids'] = [cat_id[0] for cat_id in category_ids]
            else:
                url['category_ids'] = []

            urls.append(url)

        return urls

    def product_exists(self, product_url):
        cursor = self.db.cursor()
        query = "SELECT id, status FROM product WHERE url = '" + product_url + "'"
        cursor.execute(query)
        results = cursor.fetchall()

        if cursor.rowcount == 0:
            return False

        return results

    def fetch_existing_products(self, retailer_id):
        urls = []
        query = f"SELECT p.id, p.country_id, p.url as link FROM product AS p LEFT JOIN retailer AS r ON r.id = p.retailer_id WHERE p.status = 'active' AND r.status = 'active' AND r.id = {retailer_id}"
        cursor = self.db.cursor()
        cursor.execute(query)

        for (id, country_id, link) in cursor.fetchall():
            url = {}

            url['product_id'] = id
            url['country_id'] = country_id
            url['url'] = link
            url['spider_type'] = "checker"

            urls.append(url)

        return urls

    def deactivate_product(self, product_id):
        urls = []
        query = "UPDATE product SET status = 'inactive' WHERE id = " + str(product_id)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        # print('Product deactivated')

    def store_product(self, item):
        try:
            exists = self.product_exists(item['product_url']);

            if not item['brand_name']:
                return item

            if exists:
                # print('URL already exists')
                if exists[0][1] == 'inactive':
                    # print('Updating product ' + str(exists[0][0]))
                    update_inactive_prod = "UPDATE product SET price = %s, discount = %s, status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
                    update_values = (
                        item['listed_price'],
                        item['discounted_percent'],
                        'active',
                        exists[0][0]
                    )
                    self.cursor.execute(update_inactive_prod, update_values)
                    self.db.commit()
            else:
                brand_id = self.brand_manager.get_brand(item['brand_name'])
                update_prods = "INSERT INTO product (title, url, description, price, discount, discounted_price, brandname, status, created_at, updated_at, country_id, user_id, retailer_id, related_brand_name_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s, %s, %s)"
                prods_val = (
                    item['product_name'],
                    item['product_url'],
                    item['product_desc'],
                    item['listed_price'],
                    item['discounted_percent'],
                    item['discounted_price'],
                    item['brand_name'],
                    'active',
                    item['country_id'],
                    item['user_id'],
                    item['retailer_id'],
                    brand_id
                )

                self.cursor.execute(update_prods, prods_val)
                last_product_id = self.cursor.lastrowid
                
                for i in item['category_ids']:
                    update_prod_cat = "INSERT INTO product_category (product_id, category_id) VALUES (%s, %s)"
                    prod_cat_val = (last_product_id, i)
                    self.cursor.execute(update_prod_cat, prod_cat_val)

                for i in item['prod_images']:
                    update_images = "INSERT INTO product_image (product_id, src, filesrc) VALUES (%s, %s, %s)"
                    images_val = (last_product_id, i, '')           
                    self.cursor.execute(update_images, images_val)
                
                for i in item['reviews']:
                    if (i.get('review')):
                        update_review = "INSERT INTO product_review (product_id, review, stars) VALUES (%s, %s, %s)"
                        review_val = (last_product_id, i['review'], i['stars'])
                        self.cursor.execute(update_review, review_val)
                
                self.db.commit()
                # print('Data inserted into products MariaDB')

            return item
        
        except Exception as e:
            # print(f"Error inserting data into MariaDB: {e}")
            raise DropItem("Item dropped due to database error")

        return

    def update_scrapping_url_scrapped_datetime(self, scrappingurl_id):
        update_inactive_prod = "UPDATE scrapping_urls SET last_scrapped_at = CURRENT_TIMESTAMP WHERE id = " + str(scrappingurl_id)

        self.cursor.execute(update_inactive_prod)
        self.db.commit()

        return

    def update_product(self, item):
        print('Updating product price')

        update_inactive_prod = "UPDATE product SET price = %s, discount = %s, discounted_price = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        update_values = (
            item['listed_price'],
            item['discounted_percent'],
            item['discounted_price'],
            item['product_id']
        )
        self.cursor.execute(update_inactive_prod, update_values)
        self.db.commit()

        return
