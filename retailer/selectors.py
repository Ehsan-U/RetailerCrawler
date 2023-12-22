
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


@dataclass
class PlaceDesTendancesPaths():
    """
    Xpaths for the placedestendances.com domain.
    """

    PRODUCTS = "//div[@class='product']"
    DISCOUNTED = ".//div[@class='labels text-picto']"
    PRODUCT_URL = ".//a[not(@class)]/@href"
    ELEMENT = "//div[@id='viewallPagination']/a[last()]/@data-page" # reached end when self.PAGE_NO equals the value of the element


@dataclass
class SunglassHutPaths():
    """
    Xpaths for the sunglasshut.com domain.
    """

    PRODUCTS = "//article"
    DISCOUNTED = ".//span[contains(text(), '% off')]"
    PRODUCT_URL = "./div/a/@href"
    ELEMENT = "//body" # dummy element, reached end on 2nd page