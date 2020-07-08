# Built-in libraries
import os

# Paths
SRC_PATH = os.path.dirname(os.path.dirname(__file__))
BASE_PATH = os.path.join(SRC_PATH, "base/")
CRAWLERS_PATH = os.path.join(SRC_PATH, "crawlers/")
MEMORY_PATH = os.path.join(SRC_PATH, "crawlers/memory_pickles/")

LUO_API = os.environ.get('LUO_API', 'http://localhost:8000/crawlers/')

# Error messages
REMOVE_ERROR_MSG = '`method` must be either "unicode" and "ascii", not {}'

NO_CONTENT = {
    'inmuebles24': {
        'html_element': '//div[@id="no-results"]',
        'locator': 'XPATH'
    },
    'propiedades': {
        'html_element': '//p[@class="body-modal m-t-30 "]',
        'locator': 'XPATH'
    },
    'lamudi': {
        'html_element': 'clpNoResults-text-title',
        'locator': 'CLASS_NAME'
    }
}

TEXT_BOX = {
    'inmuebles24': {
        'html_element': '//div[@class="rbt-input-hint-container"]//input',
        'locator': 'XPATH'
    },
    'propiedades': {
        'html_element': 'search-nu-input',
        'locator': 'ID'
    },
    'icasas': {
        'html_element': 'location-input',
        'locator': 'ID'
    },
    'vivanuncios': {
        'html_element': 'locationPicker-input',
        'locator': 'ID'
    },
    'lamudi': {
        'html_element': 'SearchBar-searchField',
        'locator': 'CLASS_NAME'
    }
}

SUGGESTIONS = {
    'inmuebles24': {
        'html_element': '//ul[@class="rbt-menu dropdown-menu show"]//a/span',
        'locator': 'XPATH'
    },
    'propiedades': {
        'html_element': '//a[@class="ui-corner-all"]',
        'locator': 'XPATH'
    },
    'icasas': {
        'html_element': '//div[@class="tt-suggestion"]',
        'locator': 'XPATH'
    },
    'vivanuncios': {
        'html_element': 'locationPicker-item',
        'locator': 'CLASS_NAME'
    },
    'lamudi': {
        'html_element': 'js-listItem',
        'locator': 'CLASS_NAME'
    }
}
