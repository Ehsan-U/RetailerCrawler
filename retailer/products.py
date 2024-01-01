class Products:

    def get_pages(self, spider_type):
        if (spider_type == "checker"):
            return self.fetch_existing_products()
        else:
            return self.fetch_scrapping_urls()
        pass

    def fetch_scrapping_urls(self):
        pages = [{
                "url": "https://www.amazon.fr/s?keywords=Chaussures+de+running+femme&i=fashion-womens-shoes&rh=n%3A7477793031%2Cp_n_deal_type%3A26902977031%2Cp_36%3A4000-%2Cp_n_size_two_browse-vebin%3A14223299031%2Cp_72%3A437873031&dc&c=ts&qid=1704089417&rnid=437872031&ts_id=7477793031&ref=sr_nr_p_72_1&ds=v1%3AK3K9AZ4G%2BDqLzCw66YjsbVlAZ6xnE8NpTfawjlHFY2A",
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
                'url':'https://www.amazon.fr/Mustang-1443-508-Booty-Femme-Rouge/dp/B0BWFQD5M1/ref=sr_1_6?pf_rd_i=12725743031&pf_rd_m=A1X6FK5RDHNB96&pf_rd_p=b5622614-cccb-40dc-a54e-92c09ef6efd6&pf_rd_r=E1KPVFPJXZV26N7YJY6E&pf_rd_s=merchandised-search-5&qid=1704082585&s=apparel&sr=1-6',
                'spider_type': 'checker'
            }
        ]

        return pages
