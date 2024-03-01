from mysql.connector import connect
from dotenv import load_dotenv
import os
from retailer.product_brand import ProductBrand

if __name__ == '__main__':
    load_dotenv()
    db = connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT'),
        use_pure=False
    )
    manager = ProductBrand(db)
    db.start_transaction()
    manager.update_existent()
    db.commit()
    db.close()