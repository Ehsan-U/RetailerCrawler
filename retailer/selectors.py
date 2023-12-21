
from dataclasses import dataclass



@dataclass
class IrunPaths():
    """
    Xpaths for the i-run.fr domain.
    """
    
    PRODUCTS = "//section[@class='catalog-page-section']/div"
    DISCOUNTED = ".//span[@class='prixbarre']"
    PRODUCT_URL = "./a/@href"
    ELEMENT = "//h1[text()='Erreur 404']" # reached end when exists


@dataclass
class BhvPaths():
    """
    Xpaths for the bhv.fr domain.
    """
    
    PRODUCTS = "//ul[@class='category-products']/li"
    DISCOUNTED = ".//span[contains(@class, 'product-price-old')]"
    PRODUCT_URL = ".//div[contains(@class, 'product-link')]/@data-link"
    ELEMENT = "//p[@class='category-noresults']" # reached end when exists


@dataclass
class FarfetchPaths():
    """
    Xpaths for the farfetch.com domain.
    """

    PRODUCTS = "//ul[@data-testid='product-card-list']/li/div[@itemid]"
    DISCOUNTED = ".//p[@data-component='PriceOriginal']"
    PRODUCT_URL = "./a/@href"
    ELEMENT = "//ul[@data-testid='product-card-list' and not(li)]" # reached end when exists


@dataclass
class DelseyPaths():
    """
    Xpaths for the fr.delsey.com domain.
    """

    PRODUCTS = "//div[@class='grid-item__content']"
    DISCOUNTED = ".//div[@class='grid-product__tag grid-product__tag--sale']"
    PRODUCT_URL = "./a/@href"
    ELEMENT = "//div[@class='index-section']" # reached end when exists


@dataclass
class VestiaireCollectivePaths():
    """
    Xpaths for the fr.vestiairecollective.com domain.
    """

    PRODUCTS = "//ul[contains(@class, 'product-search_catalog')]/li"
    DISCOUNTED = ".//span[contains(@class, 'price--discount')]"
    PRODUCT_URL = ".//a[not(@class)]/@href"
    ELEMENT = "//button[contains(@class, 'paginationButton--current')]" # reached end when not exists