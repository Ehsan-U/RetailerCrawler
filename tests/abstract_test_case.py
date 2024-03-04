from unittest import TestCase
import os

import mysql.connector
from dotenv import load_dotenv

from mysql.connector.connection import MySQLConnectionAbstract


class AbstractTestCase(TestCase):
    db: MySQLConnectionAbstract

    def setUp(self):
        super().setUp()
        load_dotenv('../../.env.test')
        self.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT'),
            use_pure=False
        )
        self.db.start_transaction()

    def tearDown(self):
        super().tearDown()
        self.db.rollback()
        self.db.close()
