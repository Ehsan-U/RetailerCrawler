
DOMAIN_SETTINGS = {
    'fr.vestiairecollective.com': {
        'javascript': {
            'listing_page': True,
            'product_page': False,
            'args': {
                'browserHtml': True, 
                'javascript': True,
                "actions": [
                    {"action": "waitForSelector", "selector": {"type": "xpath", "value": "//button[@title='Accepter']"}, "timeout": 10},
                    {"action": "click", "selector": {"type": "xpath", "value": "//button[@title='Accepter']"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]
            }
        },
        'selectors': {
            'PRODUCTS': "//ul[contains(@class, 'product-search_catalog')]/li[not(.//span[contains(@class, 'soldText')])]",
            "DISCOUNTED": ".//span[contains(@class, 'price--discount')]",
            "PRODUCT_URL": ".//a[not(@class)]/@href",
            "ELEMENT": "//button[contains(@class, 'paginationButton--current')]", # reached end when not exists
        },
        'end': {'condition': "element_present", 'negate': True},
    },

    'mes-bijoux.fr': {
        'javascript': {
            'listing_page': True,
            'product_page': False,
            'args': {
                'browserHtml': True, 
                'javascript': True,
            }
        },
        'selectors': {
            'PRODUCTS': "//article[@data-id-product]",
            "DISCOUNTED": ".//div[@data-action='update-price']/div/div[@class='mb-omnibus-left']",
            "PRODUCT_URL": "./div/a/@href",
            "ELEMENT": "//article[@data-id-product]", # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True}
    },

    'sunglasshut.com': {
        'javascript': {
            'listing_page': True,
            'product_page': True,
            'args': {
                'browserHtml': True, 
                'javascript': True,
                "actions":  [
                    {"action": "waitForSelector", "selector": {"type": "xpath", "value": "//div[@class='geo-buttons']/button"}, "timeout": 10},
                    {"action": "click", "selector": {"type": "xpath", "value": "//div[@class='geo-buttons']/button"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ]
            }
        },
        'selectors': {
            'PRODUCTS': "//article",
            "DISCOUNTED": ".//span[contains(text(), '% off')]",
            "PRODUCT_URL": "./div/a/@href",
            "ELEMENT": "//body", # dummy element, reached end on 1st page
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'marionnaud.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': True,
            'args': {
                'browserHtml': True, 
                'javascript': True,
            }
        },
        'selectors': {
            'PRODUCTS': "//div[contains(@class, 'product-listing-area')]//ul[@class='product-listing product-grid']/li",
            "DISCOUNTED": ".//div[@class='striked']",
            "PRODUCT_URL": "./div/a/@href",
            "ELEMENT": "//a[@class='page-link']"  # reached end when PAGE_NO greater than the length of the element
        },
        'end': {"condition": "page_no_gt_len", "negate": False}
    },

    'shoes.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='productsList']/div",
            "DISCOUNTED": ".//span[@class='productlist_prix' and not(@id)]/s",
            "PRODUCT_URL": "./div[@name='zoomInfoDiv']/a/@href",
            "ELEMENT": "//span[@class='dis_current_page']" # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True}
    },

    'spartoo.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='productsList']/div",
            "DISCOUNTED": ".//span[@class='productlist_prix' and not(@id)]/s",
            "PRODUCT_URL": "./div[@name='zoomInfoDiv']/a/@href",
            "ELEMENT": "//span[@class='dis_current_page']"  # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True}
    },

    'parfumsmoinschers.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//ul/li[@class='product']",
            "DISCOUNTED": "./span[@class='productDiscount']",
            "PRODUCT_URL": "./a[not(@class)]/@href",
            "ELEMENT": "//ul/li[@class='product']"  # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True}
    },

    'amazon.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@data-component-type='s-search-result']",
            "DISCOUNTED": ".//span[@data-a-strike]",
            "PRODUCT_URL": ".//div[@data-cy='title-recipe']/h2/a[not(contains(@href, '/click?'))]/@href",
            "ELEMENT": "//span[@class='s-pagination-strip']"  # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True},
        'page_limit': 100
    },
    
    'amazon.ca': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@data-component-type='s-search-result']",
            "DISCOUNTED": ".//span[@data-a-strike]",
            "PRODUCT_URL": ".//div[@data-cy='title-recipe']/h2/a[not(contains(@href, '/click?'))]/@href",
            "ELEMENT": "//span[@class='s-pagination-strip']"  # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True},
        'page_limit': 100
    },

    'm.darty.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[contains(@id, 'product')]",
            "DISCOUNTED": ".//div[contains(@class, 'product-price__price--is-striped')]",
            "PRODUCT_URL": ".//a[@data-automation-id='product_title']/@href",
            "ELEMENT": "//div[contains(@id, 'product')]"  # reached end when not found
        },
        'end': {'condition': "element_present", 'negate': True}
    },

    'placedestendances.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='product']",
            "DISCOUNTED": ".//div[@class='labels text-picto']",
            "PRODUCT_URL": ".//a[not(@class)]/@href",
            "ELEMENT": "//div[@id='viewallPagination']/a[last()]/@data-page" # reached end when self.PAGE_NO equals the value of the element
        },
        'end': {'condition': "page_no_eq_val", 'negate': False}
    },

    'jacadi.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='jac-product-list-item']",
            "DISCOUNTED": ".//del[@class='jac-product-price-crossed']",
            "PRODUCT_URL": "./figure/a/@href",
            "ELEMENT": "//ul[@class='jac-pagination-list']/li[last()]/*/text()" # reached end when self.PAGE_NO equals the value of the element
        },
        'end': {'condition': "page_no_eq_val", 'negate': False}
    },

    'beautysuccess.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//ol[@class='products list items product-items']/li",
            "DISCOUNTED": ".//span[@class='old-price']",
            "PRODUCT_URL": "./div/a/@href",
            "ELEMENT": "//li[@class='item current']/strong/span[2]/text()"  # reached end self.PAGE_NO greater than current
        },
        'end': {'condition': "page_no_gt_val", 'negate': False}
    },

    'bhv.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//ul[@class='category-products']/li",
            "DISCOUNTED": ".//span[contains(@class, 'product-price-old')]",
            "PRODUCT_URL": ".//div[contains(@class, 'product-link')]/@data-link",
            "ELEMENT": "//p[@class='category-noresults']",
        },
        'end': {'condition': "element_present", 'negate': False}
    },

    'fr.delsey.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='grid-item__content']",
            "DISCOUNTED": ".//div[@class='grid-product__tag grid-product__tag--sale']",
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//div[@class='index-section']" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False}
    },

    'farfetch.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//ul[@data-testid='product-card-list']/li/div[@itemid]",
            "DISCOUNTED": ".//p[@data-component='PriceOriginal']",
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//ul[@data-testid='product-card-list' and not(li)]" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
        'headers': {"Accept-Language": "fr-FR"}
    },

    'fnac.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[contains(@data-automation-id, 'product-block')]",
            "DISCOUNTED": ".//del[@class='oldPrice']",
            "PRODUCT_URL": ".//p[@class='Article-desc']/a/@href",
            "ELEMENT": "//div[contains(@class, 'noResults')]"  # reached end when found
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'generale-optique.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//a[@data-t='product-block']",
            "DISCOUNTED": ".//span[contains(@class, 'price--discount')]",
            "PRODUCT_URL": "./@href",
            "ELEMENT": "//div[@class='no-results']"  # reached end when found
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'grandoptical.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//a[@data-t='product-block']",
            "DISCOUNTED": ".//span[contains(@class, 'price--discount')]",
            "PRODUCT_URL": "./@href",
            "ELEMENT": "//div[@class='no-results']"  # reached end when found
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'intersport.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//div[@class='product-box']",
            "DISCOUNTED": ".//span[contains(@class, 'product-box__price--crossed')]",
            "PRODUCT_URL": ".//a[@class='product-box__title']/@href",
            "ELEMENT": "//div[@class='no-result']" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
        'headers': {"Referer": "https://www.intersport.fr/"},
        'zyte_extra_args': {
            "httpResponseBody": True,
            "device": "mobile",
        }
    },

    'i-run.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//section[@class='catalog-page-section']/div",
            "DISCOUNTED": ".//span[@class='prixbarre']",
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//h1[text()='Erreur 404']" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'luisaviaroma.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//article[@itemprop='itemListElement']",
            "DISCOUNTED": ".//p[count(span)=3]",
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//h1[@id='pnlFileNotFoundTitle']"  # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'nocibe.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//products-list/div[@class='proditem ']",
            "DISCOUNTED": ".//div[@class='proditem__price-strike']",
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//products-list[@displayed-products-count='0']"  # reached end when found
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'sneakersnstuff.com': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//article[@class='card product']",
            "DISCOUNTED": ".//del[@class='price__original']",
            "PRODUCT_URL": ".//h3/a/@href",
            "ELEMENT": "//article[@class='page page--empty']" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'galerieslafayette.com': {
        'javascript': {
            'listing_page': True,
            'product_page': False,
            'args': {
                'browserHtml': True, 
                'javascript': True,
                "actions": [
                    {"action": "waitForSelector", "selector": {"type": "xpath", "value": "//button[@id='popin_tc_privacy_button']"}, "timeout": 5},
                    {"action": "click", "selector": {"type": "xpath", "value": "//button[@id='popin_tc_privacy_button']"}},
                    {"action": "scrollBottom", "maxScrollCount": 1},
                ],
            }
        },
        'selectors': {
            'PRODUCTS': "//a[contains(@data-test-id, 'productcard')]",
            "DISCOUNTED": "./@href", # dummy
            "PRODUCT_URL": "./@href",
            "ELEMENT": "//div[@class='single-push__body']" # reached end when exists
        },
        'end': {'condition': "element_present", 'negate': False},
    },

    'manomano.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False
        },
        'selectors': {
            'PRODUCTS': "//a[contains(@href, '/p/')]",
            "DISCOUNTED": ".//span[@data-testid='price-retail']", 
            "PRODUCT_URL": "./@href",
            "ELEMENT": "//span[text()='Pagination']" # reached end when not exists
        },
        'end': {'condition': "element_present", 'negate': True},
    },

    'asos.com': {
        'javascript': {
            'listing_page': False,
            'product_page': True,
            'args': {
                'browserHtml': True, 
                'javascript': True,
            }
        },
        'selectors': {
            'PRODUCTS': "//article",
            "DISCOUNTED": ".//span[contains(@class, 'reducedPrice')]", 
            "PRODUCT_URL": "./a/@href",
            "ELEMENT": "//a[@data-auto-id='loadMoreProducts']" # reached end when not exists
        },
        'end': {'condition': "element_present", 'negate': True},
    },
    
    'footlocker.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': True,
            'args': {
                'browserHtml': True, 
                'javascript': True,
                "actions": [
                    {"action": "waitForTimeout","timeout": 5,"onError": "return"}
                ]
            }
        },
        'selectors': {
            'PRODUCTS': "//div[contains(@class, 'ProductCard')]/a",
            "DISCOUNTED": ".//span[@class='ProductPrice-original']", 
            "PRODUCT_URL": "./@href",
            "ELEMENT": "//li[contains(@class, 'Pagination-option--next')]/a" # reached end when not exists
        },
        'end': {'condition': "element_present", 'negate': True},
    },

    'carrefour.fr': {
        'javascript': {
            'listing_page': True,
            'product_page': True,
            'args': {
                'browserHtml': True, 
                'javascript': True,
                "actions": [
                    {"action":"waitForTimeout","timeout": 5,"onError": "return"},
                    {"action":"click","selector": {"type": "xpath","value":"//div[@id='product-characteristics-table']//button[1]"}, "onError": "return"}
                ]
            }
        },
        'selectors': {
            'PRODUCTS': "//article",
            "DISCOUNTED": ".//div[contains(@class, 'product-price__amount--old')]", 
            "PRODUCT_URL": ".//a[@data-testid='product-card-title']/@href",
            "ELEMENT": "//article" # reached end when not exists
        },
        'end': {'condition': "element_present", 'negate': True},
    },

    '3suisses.fr': {
        'javascript': {
            'listing_page': False,
            'product_page': False,
        },
        'selectors': {
            'PRODUCTS': "//article[@class='item--product']",
            "DISCOUNTED": ".//span[contains(@class, 'item__price--old-box')]", 
            "PRODUCT_URL": ".//p[@class='item__title ']/a/@href",
            "ELEMENT": "//a[@class=' noDisplay ' and text()='Voir la suite']"  # reached end when found
        },
        'end': {'condition': "element_present", 'negate': False},
    }
}
