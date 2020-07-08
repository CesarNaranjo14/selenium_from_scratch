# Built-in libraries
import re

# Crawlers urls
CRAWLERS_URLS = {
    "lamudi": "https://www.lamudi.com.mx",
}

# Dicts of html_elements to scrap
AMENITIES = {
    'inmuebles24': {
        'html_element': '//section[@class="general-section article-section"]//li',
        'locator': 'XPATH'
    },
    'icasas': {
        'html_element': '//div[@class="info"]//li[@class="tick"]',
        'locator': 'XPATH'
    },
    'vivanuncios': {
        'html_element': '//div[@class="amenities-label"]',
        'locator': 'XPATH'
    }
}

STREET_MAP = {
    'inmuebles24': {
        'html_element': '//img[@class="static-map"]',
        'locator': 'XPATH'
    },
    'icasas': {
        'html_element': "see-map",
        'locator': "CLASS_NAME"
    },
    'vivanuncios': {
        'html_element': "signed-map-image",
        'locator': 'CLASS_NAME'
    }
}
