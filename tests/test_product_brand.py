from tests.abstract_test_case import AbstractTestCase
from retailer.product_brand import ProductBrand
from retailer.product_brand import normalise_name


class TestProductBrand(AbstractTestCase):
    def test_get_brand(self):
        manager = ProductBrand(self.db)

        brand_id = manager.get_brand('My Brand')
        self.assertIsInstance(brand_id, int)

        another_brand_id = manager.get_brand('Another Brand')
        self.assertIsInstance(another_brand_id, int)
        self.assertNotEqual(brand_id, another_brand_id)

        dup_brand = manager.get_brand('my_brand')
        self.assertEqual(brand_id, dup_brand)

    def test_normalisation(self):
        self.assertEqual('mybrand', normalise_name('My Brand'))
        self.assertEqual('myandbrand', normalise_name('My & Brand'))
        self.assertEqual('myssraeiu', normalise_name('MÝ ßRæïü'))

    def test_product_update(self):
        fixtures = self.db.cursor()

        fixtures.execute('''
                INSERT INTO user(
                    firstname, lastname, email, password, roles, city,
                    created_at, status, email_validation_token, website,
                    logo
                )
                VALUES ('', '', 'user@test.te', '', '[]', '', CURRENT_TIMESTAMP, '', '', '', '')
        ''')

        fixtures.execute('''
                INSERT INTO product(
                    title, user_id, brandname, url, description, price,
                    discount, status, created_at, updated_at, discounted_price
                )
                VALUES ('Prod1', %s, 'My Brand', '', '', 0, 0, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0),
                       ('Prod2', %s, 'my_brand', '', '', 0, 0, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0),
                       ('Prod3', %s, 'Another Brand', '', '', 0, 0, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)
            ''',
            (fixtures.lastrowid, fixtures.lastrowid, fixtures.lastrowid)
        )
        manager = ProductBrand(self.db)
        manager.update_existent()

        fixtures.execute('''
            SELECT p.title, b.name
            FROM product AS p
                 JOIN brand AS b ON b.id = p.brand_id
        ''')
        data = fixtures.fetchall()
        self.assertGreater(len(data), 0)
        for (title, brand_name) in data:
            if title == 'Prod1' or title == 'Prod2':
                self.assertEqual('My Brand', brand_name)
            else:
                self.assertEqual('Another Brand', brand_name)
