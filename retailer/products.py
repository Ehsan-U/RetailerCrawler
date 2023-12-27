class Products:

    def get_urls(self, type):
        if (type == "product_check"):
            return self.fetch_existing_products()
        else:
            return self.fetch_scrapping_urls()
        pass

    def fetch_scrapping_urls(self):
        pages = [
            {
                "url": "https://www.sunglasshut.com/fr/lunettes-de-soleil-femme?facet=Vente%3ATRUE",
                "user_id": 1,
                "country_id": 75,
                "retailer_id": 1,
                "category_ids": [1,2],
                "type": "scrapping"
            }
        ]

        return pages

    def fetch_existing_products(self):
        pages = [
            {
                'id': 1,
                'country_id': 231,
                'url': 'https://www.jacadi.fr/outlet/Gants-enfant-fille/p/2030919_830',
                'type': 'product'
            }
        ]

        return pages
