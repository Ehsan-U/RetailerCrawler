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
        brand_id = self._fetch_brand(norm_name)
        if brand_id > 0:
            return brand_id

        self.cursor.execute('''
                INSERT IGNORE INTO brand(name, status, normalized_name)
                VALUES (%s, 'active', %s)
            ''',
            (name, norm_name)
        )
        brand_id = self.cursor.lastrowid
        if brand_id > 0:
            return brand_id
        return self._fetch_brand(norm_name)

    def _fetch_brand(self, norm_name: str) -> int:
        self.cursor.execute('SELECT id FROM brand WHERE normalized_name = %s', (norm_name,))
        res = self.cursor.fetchall()
        return res[0][0] if len(res) > 0 else 0

    def update_existent(self):
        self.cursor.execute('SELECT id, brandname FROM product')

        for (product_id, brand_name) in self.cursor.fetchall():
            brand_id = self.get_brand(brand_name)
            self.cursor.execute('''
                UPDATE product
                SET brand_id = %s
                WHERE id = %s
            ''', (product_id, brand_id))
