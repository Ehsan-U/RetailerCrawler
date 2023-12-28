import os
from dotenv import load_dotenv
import mysql.connector

class Products:
    db = ""
    cursor = ""

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
    
    def get_urls(self, scrappingtype):
        if (scrappingtype == "product_check"):
            return self.fetch_existing_products()
        else:
            return self.fetch_scrapping_urls()
        pass

    def fetch_scrapping_urls(self):
        urls = []
        query = "SELECT su.id, su.user_id, su.country_id, su.url as link, su.retailer_id FROM scrapping_urls AS su LEFT JOIN retailer AS r ON r.id = su.retailer_id WHERE su.status = 'active' AND r.status = 'active';"
        cursor = self.db.cursor()
        cursor.execute(query)

        for (_id, user_id, country_id, link, retailer_id) in cursor.fetchall():
            url = {}
           
            url['user_id'] = user_id
            url['country_id'] = country_id
            url['url'] = link
            url['retailer_id'] = retailer_id
            url['scrappingtype'] = "scrapping"

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

    def fetch_existing_products(self):
        urls = []
        query = "SELECT p.id, p.country_id, p.url as link FROM product AS p LEFT JOIN retailer AS r ON r.id = p.retailer_id WHERE p.status = 'active' AND r.status = 'active'"
        cursor = self.db.cursor()
        cursor.execute(query)

        for (id, country_id, link) in cursor.fetchall():
            url = {}
           
            url['id'] = id
            url['country_id'] = country_id
            url['url'] = link
            url['scrappingtype'] = "product_check"

            urls.append(url)

        return urls

    def deactivate_product(self, product_id):
        urls = []
        query = "UPDATE product SET status = 'inactive' WHERE id = " + str(product_id)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()
        print('Product deactivated')