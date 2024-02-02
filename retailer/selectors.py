
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

    PRODUCTS = "//div[@class='product-box']"
    DISCOUNTED = ".//span[contains(@class, 'product-box__price--crossed')]"
    PRODUCT_URL = ".//a[@class='product-box__title']/@href"
    ELEMENT = "//div[@class='no-result']" # reached end when exists


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
    ELEMENT = "//span[@class='s-pagination-strip']"  # reached end when not found


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


@dataclass
class GrandOpticalPaths():
    """
    Xpaths for the grandoptical.com domain
    """

    PRODUCTS = "//a[@data-t='product-block']"
    DISCOUNTED = ".//span[contains(@class, 'price--discount')]"
    PRODUCT_URL = "./@href"
    ELEMENT = "//div[@class='no-results']"  # reached end when found


@dataclass
class GeneraleOptiquePaths():
    """
    Xpaths for the generale-optique.com domain
    """

    PRODUCTS = "//a[@data-t='product-block']"
    DISCOUNTED = ".//span[contains(@class, 'price--discount')]"
    PRODUCT_URL = "./@href"
    ELEMENT = "//div[@class='no-results']"  # reached end when found


@dataclass
class MesBijouxPaths():
    """
    Xpaths for the mes-bijoux.fr domain
    """

    PRODUCTS = "//article[@data-id-product]"
    DISCOUNTED = ".//div[@data-action='update-price']/div/div[@class='mb-omnibus-left']"
    PRODUCT_URL = "./div/a/@href"
    ELEMENT = "//article[@data-id-product]"  # reached end when not found


@dataclass
class ParfumsMoinsChersPaths():
    """
    Xpaths for the parfumsmoinschers.com domain
    """

    PRODUCTS = "//ul/li[@class='product']"
    DISCOUNTED = "./span[@class='productDiscount']"
    PRODUCT_URL = "./a[not(@class)]/@href"
    ELEMENT = "//ul/li[@class='product']"  # reached end when not found


@dataclass
class SuissesPaths():
    """
    Xpaths for the 3suisses.fr domain
    """
     
    PRODUCTS = "//article[@class='item--product']"
    DISCOUNTED = ".//span[contains(@class, 'item__price--old-box')]"
    PRODUCT_URL = ".//p[@class='item__title ']/a/@href"
    ELEMENT = "//a[@class=' noDisplay ' and text()='Voir la suite']"  # reached end when found


@dataclass
class DartyPaths():
    """
    Xpaths for the darty.com domain
    """

    PRODUCTS = "//div[@class='product_wrapper']"
    DISCOUNTED = ".//div[contains(@class, 'product-price__price--is-striped')]"
    PRODUCT_URL = ".//a[@data-automation-id='product_title']/@href"
    ELEMENT = "//div[contains(@class, 'no_result')]"  # reached end when found


@dataclass
class FnacPaths():
    """
    Xpaths for the fnac.com domain
    """

    PRODUCTS = "//div[contains(@data-automation-id, 'product-block')]"
    DISCOUNTED = ".//del[@class='oldPrice']"
    PRODUCT_URL = ".//p[@class='Article-desc']/a/@href"
    ELEMENT = "//div[contains(@class, 'noResults')]"  # reached end when found