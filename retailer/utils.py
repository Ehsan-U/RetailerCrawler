from price_parser import Price
from urllib.parse import urlencode, urlsplit, urlunsplit, unquote



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

    discounted_percent = ((listed_price - discounted_price) / listed_price) * 100

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

    if ('i-run.fr' in netloc):
        params = dict(qc.split("=") for qc in query.split("&")) if query else {}
        params["page"] = str(page_no)
        updated_query = urlencode(params)
        updated_url = urlunsplit((scheme, netloc, path, updated_query, fragment))
        
    elif ('bhv.fr' in netloc):
        updated_url = f"{url.rstrip('/')}/p:{page_no}"

    elif ('farfetch.com' in netloc):
        params = dict(qc.split("=") for qc in query.split("&")) if query else {}
        params["page"] = str(page_no)
        params['discount'] = unquote(params.get('discount', ''))
        updated_query = urlencode(params)
        updated_url = urlunsplit((scheme, netloc, path, updated_query, fragment))

    return updated_url



