# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from deelio.products import Products


class RetailerPipeline:
    def __init__(self):
        load_dotenv()
        DB_HOST = os.getenv('DB_HOST')
        DB_NAME = os.getenv('DB_NAME')
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')

        self.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=3306,
            use_pure=False
        )
        self.cursor = self.db.cursor()

        self.products = Products();

    def process_item(self, item, spider):
        if (item.get("scrappingtype") == "product_check"):
            self.check_discount(item)
        else:
            self.process_product(item)

        return item

    def check_discount(self, item):
        if (!item['discounted']):
            self.products.deactivate_product(item['id'])

        return

    def process_product(self, item):
        try:
            exists = self.products.product_exists(item['product_url']);

            if exists:
                print('URL already exists')
                if exists[0][1] == 'inactive':
                    print('Updating product ' + str(exists[0][0]))
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
                update_prods = "INSERT INTO product (title, url, description, price, discount, brandname, status, created_at, updated_at, country_id, brand_id, retailer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s, %s)"
                prods_val = (
                    item['product_name'],
                    item['product_url'],
                    item['product_desc'],
                    item['listed_price'],
                    item['discounted_percent'],
                    item['brand_name'],
                    'active',
                    item['country_id'],
                    item['user_id'],
                    item['retailer_id']
                )

                self.cursor.execute(update_prods, prods_val)
                last_product_id = self.cursor.lastrowid
                
                for i in item['category_ids']:
                    update_prod_cat = "INSERT INTO product_category (product_id, category_id) VALUES (%s, %s)"
                    prod_cat_val = (last_product_id, i)
                    self.cursor.execute(update_prod_cat, prod_cat_val)

                for i in item['reviews']:
                    update_images = "INSERT INTO product_image (product_id, src, filesrc) VALUES (%s, %s, %s)"
                    images_val = (last_product_id, i, '')           
                    self.cursor.execute(update_images, images_val)
                
                for i in item['reviews']:
                    update_review = "INSERT INTO product_review (product_id, review, stars) VALUES (%s, %s, %s)"
                    review_val = (last_product_id, i['review'], i['stars'])
                    self.cursor.execute(update_review, review_val)
                
                self.db.commit()
                print('Data inserted into products MariaDB')

            return item
        
        except Exception as e:
            print(f"Error inserting data into MariaDB: {e}")
            raise DropItem("Item dropped due to database error")

        return
