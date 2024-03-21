# Scrapy settings for retailer project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from dotenv import load_dotenv
from web_poet import ApplyRule

from retailer.page_objects.pages import ProductPage
from retailer.page_objects.fr.irun import IRunProduct
from retailer.page_objects.fr.bhv import BhvProduct
from retailer.page_objects.fr.farfetch import FarfetchProduct
from retailer.page_objects.fr.delsey import DelseyProduct
from retailer.page_objects.fr.vestiairecollective import VestiaireCollectiveProduct
from retailer.page_objects.fr.placedestendances import PlaceDestendancesProduct
from retailer.page_objects.fr.sunglasshut import SunglasshutProduct
from retailer.page_objects.fr.jacadi import JacadiProduct
from retailer.page_objects.fr.sneakersnstuff import SneakersnStuffProduct
from retailer.page_objects.fr.luisaviaroma import LuisaViaRomaProduct
from retailer.page_objects.fr.intersport import IntersportProduct
from retailer.page_objects.fr.marionnaud import MarionnaudProduct
from retailer.page_objects.fr.amazon import AmazonProduct
from retailer.page_objects.fr.shoes import ShoesProduct
from retailer.page_objects.fr.spartoo import SpartooProduct
from retailer.page_objects.fr.grandoptical import GrandOpticalProduct
from retailer.page_objects.fr.generaleoptique import GeneraleOptiqueProduct
from retailer.page_objects.fr.mesbijoux import MesBijouxProduct
from retailer.page_objects.fr.parfumsmoinschers import ParfumsMoinsChersProduct
from retailer.page_objects.fr.suisses import SuissesProduct
from retailer.page_objects.fr.darty import DartyProduct
from retailer.page_objects.fr.fnac import FnacProduct
from retailer.page_objects.fr.nocibe import NocibeProduct
from retailer.page_objects.fr.beautysuccess import BeautySuccessProduct
from retailer.page_objects.fr.galerieslafayette import GalerieslaFayetteProduct
from retailer.page_objects.fr import manomano as fr_manomano
from retailer.page_objects.fr import asos as fr_asos
from retailer.page_objects.fr import footlocker as fr_footlocker
from retailer.page_objects.fr import carrefour as fr_carrefour

from retailer.page_objects.ca import amazon as ca_amazon

load_dotenv() 

BOT_NAME = "retailer"

SPIDER_MODULES = ["retailer.spiders"]
NEWSPIDER_MODULE = "retailer.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "retailer (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "retailer.middlewares.RetailerSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "retailer.middlewares.RetailerDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "retailer.pipelines.RetailerPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
    "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy_poet.InjectionMiddleware": 543,
    "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000,
}

SPIDER_MIDDLEWARES = {
    "scrapy_poet.RetryMiddleware": 275,
}

REQUEST_FINGERPRINTER_CLASS = "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter"
ZYTE_API_KEY = os.getenv("ZYTE_API")
ZYTE_API_TRANSPARENT_MODE = True


SCRAPY_POET_RULES = [
    ApplyRule("i-run.fr", use=IRunProduct, instead_of=ProductPage),
    ApplyRule("bhv.fr", use=BhvProduct, instead_of=ProductPage),
    ApplyRule("farfetch.com", use=FarfetchProduct, instead_of=ProductPage),
    ApplyRule("fr.delsey.com", use=DelseyProduct, instead_of=ProductPage),
    ApplyRule("fr.vestiairecollective.com", use=VestiaireCollectiveProduct, instead_of=ProductPage),
    ApplyRule("placedestendances.com", use=PlaceDestendancesProduct, instead_of=ProductPage),
    ApplyRule("sunglasshut.com", use=SunglasshutProduct, instead_of=ProductPage),
    ApplyRule("jacadi.fr", use=JacadiProduct, instead_of=ProductPage),
    ApplyRule("sneakersnstuff.com", use=SneakersnStuffProduct, instead_of=ProductPage),
    ApplyRule("luisaviaroma.com", use=LuisaViaRomaProduct, instead_of=ProductPage),
    ApplyRule("intersport.fr", use=IntersportProduct, instead_of=ProductPage),
    ApplyRule("marionnaud.fr", use=MarionnaudProduct, instead_of=ProductPage),
    ApplyRule("amazon.fr", use=AmazonProduct, instead_of=ProductPage),
    ApplyRule("amazon.ca", use=ca_amazon.AmazonProduct, instead_of=ProductPage),
    ApplyRule("shoes.fr", use=ShoesProduct, instead_of=ProductPage),
    ApplyRule("spartoo.com", use=SpartooProduct, instead_of=ProductPage),
    ApplyRule("grandoptical.com", use=GrandOpticalProduct, instead_of=ProductPage),
    ApplyRule("generale-optique.com", use=GeneraleOptiqueProduct, instead_of=ProductPage),
    ApplyRule("mes-bijoux.fr", use=MesBijouxProduct, instead_of=ProductPage),
    ApplyRule("parfumsmoinschers.com", use=ParfumsMoinsChersProduct, instead_of=ProductPage),
    ApplyRule("3suisses.fr", use=SuissesProduct, instead_of=ProductPage),
    ApplyRule("m.darty.com", use=DartyProduct, instead_of=ProductPage),
    ApplyRule("fnac.com", use=FnacProduct, instead_of=ProductPage),
    ApplyRule("nocibe.fr", use=NocibeProduct, instead_of=ProductPage),
    ApplyRule("beautysuccess.fr", use=BeautySuccessProduct, instead_of=ProductPage),
    ApplyRule("galerieslafayette.com", use=GalerieslaFayetteProduct, instead_of=ProductPage),
    ApplyRule("manomano.fr", use=fr_manomano.ManomanoProduct, instead_of=ProductPage),
    ApplyRule("asos.com", use=fr_asos.AsosProduct, instead_of=ProductPage),
    ApplyRule("footlocker.fr", use=fr_footlocker.FootlockerProduct, instead_of=ProductPage),
    ApplyRule("carrefour.fr", use=fr_carrefour.CarrefourProduct, instead_of=ProductPage)
]

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [403, 520, 521, 304]
REDIRECT_ENABLED = False


GEOLOCATIONS = {
    75: "FR",
    231: "US",
    37:"CA"
}
