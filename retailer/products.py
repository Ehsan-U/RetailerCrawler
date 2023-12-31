class Products:

    def get_pages(self, spider_type):
        if (spider_type == "checker"):
            return self.fetch_existing_products()
        else:
            return self.fetch_scrapping_urls()
        pass

    def fetch_scrapping_urls(self):
        pages = [
            {
                "url": "https://www.marionnaud.fr/soin-visage/anti-rides-et-anti-age/soin-de-jour/c/V0301",
                "user_id": 1,
                "country_id": 75,
                "retailer_id": 1,
                "category_ids": [1,2],
                "spider_type": "scraper"
            }
        ]

        return pages

    def fetch_existing_products(self):
        pages = [
            {
                'id': 1,
                'country_id': 231,
                'url': 'https://www.marionnaud.fr/soin-visage/anti-rides-et-anti-age/soin-de-jour/absolue-creme-anti-age-absolue-creme-fondante-regenerante-illuminatrice-lancome/p/101577239',
                'spider_type': 'checker'
            }
        ]

        return pages
