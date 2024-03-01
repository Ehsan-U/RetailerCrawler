from mysql.connector.connection import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.cursor import MySQLCursorAbstract
from unidecode import unidecode
import re


def normalise_name(name: str) -> str:
    name = unidecode(name).lower().replace('&', 'and')
    return re.sub(r'[^0-9a-z]', '', name)


class ProductBrand:
    db: MySQLConnectionAbstract | PooledMySQLConnection
    cursor: MySQLCursorAbstract

    def __init__(self, conn: MySQLConnectionAbstract | PooledMySQLConnection):
        self.db = conn
        self.cursor = conn.cursor()

    def get_brand(self, name: str) -> int:
        norm_name = normalise_name(name)

        self.cursor.execute(
            'INSERT IGNORE INTO product_brand_name(displayed_name, normalised_name) VALUES (%s, %s)',
            (name, norm_name)
        )
        brand_id = self.cursor.lastrowid
        if brand_id != 0:
            return brand_id

        self.cursor.execute('SELECT id FROM product_brand_name WHERE normalised_name = %s', (norm_name,))
        res = self.cursor.fetchall()
        return res[0][0]

    def update_existent(self):
        self.cursor.execute('SELECT id, brandname FROM product')

        data = []
        for row in self.cursor.fetchall():
            data.append(row)

        self.__make_tmp_table()

        batch = 0
        brands = []
        products = []
        for (product_id, brand_name) in data:
            norm_name = normalise_name(brand_name)
            brands.extend([brand_name, norm_name])
            products.extend([product_id, norm_name])
            batch += 1
            if batch > 50:
                self.__flush_batch(brands, products)
                batch = 0
                brands = []
                products = []

        self.__flush_batch(brands, products)
        self.__finalise_update()

    def __make_tmp_table(self):
        tmp_cursor = self.db.cursor()
        tmp_cursor.execute('''
            CREATE TEMPORARY TABLE tmp_product_brand(
                product_id INT, brand_name VARCHAR(64),
                PRIMARY KEY (product_id) USING BTREE,
                INDEX brand_name (brand_name) USING BTREE
            )
        ''')

    def __finalise_update(self):
        insert_cursor = self.db.cursor()
        insert_cursor.execute('''
            UPDATE product AS p
                   JOIN tmp_product_brand AS tpb ON tpb.product_id = p.id
                   JOIN product_brand_name AS pbn ON pbn.normalised_name = tpb.brand_name
            SET p.related_brand_name_id = pbn.id
        ''')
        insert_cursor.execute('DROP TEMPORARY TABLE tmp_product_brand')

    def __flush_batch(self, brands: list, products: list):
        if len(brands) == 0 or len(products) == 0:
            return
        insert_cursor = self.db.cursor()
        query = 'INSERT IGNORE INTO product_brand_name(displayed_name, normalised_name) VALUES '
        query += '(%s, %s),' * int(len(brands) / 2)
        insert_cursor.execute(query.rstrip(','), brands)

        query = 'INSERT INTO tmp_product_brand(product_id, brand_name) VALUES '
        query += '(%s, %s),' * int(len(products) / 2)
        insert_cursor.execute(query.rstrip(','), products)
