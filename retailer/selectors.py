
from dataclasses import dataclass


@dataclass
class IrunPaths():
    """
    Xpaths for the i-run.fr domain.
    """
    
    PRODUCTS = "//section[@class='catalog-page-section']/div"
    DISCOUNTED = ".//span[@class='prixbarre']"
    PRODUCT_URL = "./a/@href"
    LAST_PAGE = "//h1[text()='Erreur 404']"


@dataclass
class BhvPaths():
    """
    Xpaths for the bhv.fr domain.
    """
    
    PRODUCTS = "//ul[@class='category-products']/li"
    DISCOUNTED = ".//span[contains(@class, 'product-price-old')]"
    PRODUCT_URL = ".//div[contains(@class, 'product-link')]/@data-link"
    LAST_PAGE = "//p[@class='category-noresults']"


@dataclass
class FarfetchPaths():
    """
    Xpaths for the farfetch.com domain.
    """

    PRODUCTS = "//ul[@data-testid='product-card-list']/li/div[@itemid]"
    DISCOUNTED = ".//p[@data-component='PriceOriginal']"
    PRODUCT_URL = "./a/@href"
    LAST_PAGE = "//ul[@data-testid='product-card-list' and not(li)]"