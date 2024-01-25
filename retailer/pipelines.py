# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from retailer.products import Products


class RetailerPipeline:
    def __init__(self):
        self.products = Products();

    def process_item(self, item, spider):
        if (item.get("spider_type") == "checker"):
            if (item.get('discounted_flag') == False):
                self.products.deactivate_product(item['product_id'])
        else:
            self.products.store_product(item)

        return item
