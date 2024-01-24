from price_parser import Price
from urllib.parse import urlencode, urlsplit, urlunsplit, unquote, unquote_plus


def calculate_discount(discounted_price: str, listed_price: str):
    """
    Calculate the percentage discount between the discounted price and the listed price.

    Args:
        discounted_price (str): The discounted price.
        listed_price (str): The listed price.

    Returns:
        float: The percentage discount between the discounted price and the listed price.
    """
    if discounted_price is None:
        return float(0)

    discounted_price = Price.fromstring(discounted_price).amount_float
    listed_price = Price.fromstring(listed_price).amount_float

    try:
        discounted_percent = ((listed_price - discounted_price) / listed_price) * 100
    except TypeError:
        return float(0)

    return round(discounted_percent)



def build_paginated_url(url: str, page_no: int):
    """
    Build a paginated URL by appending the page number to the given URL.

    Args:
        url (str): The original URL.
        page_no (int): The page number to be appended.

    Returns:
        str: The updated paginated URL.
    """
    scheme, netloc, path, query, fragment = urlsplit(url)
    params = dict((qc.split("=") if "=" in qc else (qc, "") for qc in query.split("&"))) if query else {}

    if ('i-run.fr' in netloc) or ('fr.delsey.com' in netloc):
        params["page"] = str(page_no)
        query = urlencode(params)

    elif ('bhv.fr' in netloc):
        path = path.rstrip('/') + f"/p:{page_no}"

    elif ('farfetch.com' in netloc):
        params = dict(qc.split("=") for qc in query.split("&")) if query else {}
        params["page"] = str(page_no)
        params['discount'] = unquote(params.get('discount', ''))
        query = urlencode(params)

    elif ("fr.vestiairecollective.com" in netloc):
        path = path.rstrip('/') + f"/p-{page_no}/"

    elif ("placedestendances.com" in netloc):
        path = path.rstrip('/') + f"/page/{page_no}"

    elif ("sunglasshut.com" in netloc):
        static_page_value = 50 # get all products at once on 2nd page
        params["currentPage"] = str(static_page_value)
        query = urlencode(params)

    elif ("jacadi.fr" in netloc):
        params = dict(qc.split("=") for qc in query.split("&")) if query else {}
        params['q'] = ":score-jacadi-fr"
        params["page"] = str(page_no-1)
        query = urlencode(params)

    elif ("sneakersnstuff.com" in netloc):
        path = path.rstrip('/') + f"/{page_no}"

    elif ("luisaviaroma.com" in netloc):
        params["Page"] = str(page_no)
        query = urlencode(params)

    elif ("intersport.fr" in netloc or "grandoptical.com" in netloc):
        params["page"] = str(page_no)
        query = urlencode(params)

    elif ("marionnaud.fr" in netloc):
        params["page"] = str(page_no-1)
        params["pageSize"] = 100
        params['q'] = ':rank-desc'
        query = urlencode(params)

    elif ("amazon.fr" in netloc):
        params["page"] = str(page_no)
        params["ref"] = f"sr_pg_{str(page_no)}"
        query = unquote_plus(urlencode(params))

    elif ("shoes.fr" in netloc or "spartoo.com" in netloc):
        url = url.replace("php#", "php?")
        scheme, netloc, path, query, fragment = urlsplit(url)
        params = dict((qc.split("=") if "=" in qc else (qc, "") for qc in query.split("&"))) if query else {}
        params['offset'] = 144 * (page_no - 1)
        query = urlencode(params)

    elif ("generale-optique.com" in netloc):
        if "&page" in url:
            url = url.split("&page")[0]
        url += f"&page={page_no}"
        return url

    elif ("mes-bijoux.fr" in netloc):
        params['p'] = str(page_no)
        query = urlencode(params)

    updated_url = urlunsplit((scheme, netloc, path, query, fragment))
    return updated_url



