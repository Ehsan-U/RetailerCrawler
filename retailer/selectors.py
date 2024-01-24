
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

    PRODUCTS = "//ul[contains(@class, 'product-search_catalog')]/li[not(.//span[contains(@class, 'soldText')])]"
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
    ELEMENT = "//body" # dummy element, reached end on 1st page


@dataclass
class JacadiPaths():
    """
    Xpaths for the jacadi.fr domain.
    """

    PRODUCTS = "//div[@class='jac-product-list-item']"
    DISCOUNTED = ".//del[@class='jac-product-price-crossed']"
    PRODUCT_URL = "./figure/a/@href"
    ELEMENT = "//ul[@class='jac-pagination-list']/li[last()]/*/text()" # reached end when self.PAGE_NO equals the value of the element


@dataclass
class SneakersnStuffPaths():
    """
    Xpaths for the sneakersnstuff.com domain.
    """

    PRODUCTS = "//article[@class='card product']"
    DISCOUNTED = ".//del[@class='price__original']"
    PRODUCT_URL = ".//h3/a/@href"
    ELEMENT = "//article[@class='page page--empty']" # reached end when exists


@dataclass
class LuisaViaRomaPaths():
    """
    Xpaths for the luisaviaroma.com domain.
    """

    PRODUCTS = "//article[@itemprop='itemListElement']"
    DISCOUNTED = ".//p[count(span)=3]"
    PRODUCT_URL = "./a/@href"
    ELEMENT = "//h1[@id='pnlFileNotFoundTitle']"  # reached end when exists


@dataclass
class IntersportPaths():
    """
    Xpaths for the intersport.fr domain.
    """

    PRODUCTS = "//div[@id='productList']/div"
    DISCOUNTED = ".//span[contains(@class, 'price--suggested')]"
    PRODUCT_URL = ".//div[@class='product-card__title']/a[@class='product-url']/@href"
    ELEMENT = "//h1[@class='notfound']" # reached end when exists


@dataclass
class MarionnaudPaths():
    """
    Xpaths for the marionnaud.fr domain.
    """

    PRODUCTS = "//div[contains(@class, 'product-listing-area')]//ul[@class='product-listing product-grid']/li"
    DISCOUNTED = ".//div[@class='striked']"
    PRODUCT_URL = "./div/a/@href"
    ELEMENT = "//a[@class='page-link']"  # reached end when PAGE_NO greater than the length of the element


@dataclass
class AmazonPaths():
    """
    Xpaths for the amazon.fr domain.
    """

    PRODUCTS = "//div[@data-component-type='s-search-result']"
    DISCOUNTED = ".//span[@data-a-strike]"
    PRODUCT_URL = ".//div[@data-cy='title-recipe']/h2/a[not(contains(@href, '/click?'))]/@href"
    ELEMENT = "//span[contains(text(), 'Pas de résultats pour') or contains(text(), 'Essayez de vérifier votre orthographe')]"  # reached end when found


@dataclass
class ShoesPaths():
    """
    Xpaths for the shoes.fr domain
    """

    PRODUCTS = "//div[@class='productsList']/div"
    DISCOUNTED = ".//span[@class='productlist_prix' and not(@id)]/s"
    PRODUCT_URL = "./div[@name='zoomInfoDiv']/a/@href"
    ELEMENT = "//span[@class='dis_current_page']" # reached end when not found


@dataclass
class SpartooPaths():
    """
    Xpaths for the spartoo.com domain
    """

    PRODUCTS = "//div[@class='productsList']/div"
    DISCOUNTED = ".//span[@class='productlist_prix' and not(@id)]/s"
    PRODUCT_URL = "./div[@name='zoomInfoDiv']/a/@href"
    ELEMENT = "//span[@class='dis_current_page']"  # reached end when not found