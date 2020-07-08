# Built-in libraries
import os
import unicodedata

# Third-party libraries
from selenium import webdriver

# Modules
from .constants import (
    CRAWLERS_PATH,
    REMOVE_ERROR_MSG,
)


def format_data():
    data = dict()

    # Comparables general data
    data["publication_name"] = None
    data["description"] = None
    data["url"] = None
    data["price"] = None
    data["currency"] = None
    data["in_real_state_development"] = 0
    data["operation"] = None
    data["property_type"] = None
    data["website"] = None
    data["development"] = None  # string

    # Address
    data["address"] = {}
    data["address"]["street"] = None  # str
    data["address"]["ext_number"] = None  # str
    data["address"]["neighborhood"] = None  # str
    data["address"]["municipality"] = None  # str
    data["address"]["state"] = None  # str
    data["address"]["city"] = None  # str
    data["address"]["country"] = None  # str
    data["address"]["zip_code"] = None  # int
    data["address"]["latitude"] = None  # float
    data["address"]["longitude"] = None  # float

    # Property Detail
    data["propertydetail"] = {}
    data["propertydetail"]["bedrooms"] = 0  # int
    data["propertydetail"]["parking_spaces"] = 0  # int
    data["propertydetail"]["bathrooms"] = 0  # int
    data["propertydetail"]["half_bathrooms"] = 0  # int
    data["propertydetail"]["construction"] = 0  # float
    data["propertydetail"]["terrain"] = 0  # float
    # data["propertydetail"]['property_type'] = None
    data["propertydetail"]["floors"] = 0  # int
    data["propertydetail"]["age"] = 0  # string

    # Amenities
    data["amenities"] = None  # Set/List with strings

    return data


def catalogue_operation(value):
    cat_operation = {"venta": "1", "renta": "2"}
    return cat_operation[value]


def catalogue_website(value):
    cat_website = {
        "lamudi": "1",
        "casasyterrenos": "2",
        "propiedades": "3",
        "icasas": "4",
        "inmuebles24": "5",
        "vivanuncios": "6",
    }
    return cat_website[value]


def catalogue_property_type(value):
    cat_property_type = {
        "departamento": "1",
        "casa": "2",
        "terreno": "3",
        "desarrollo": "4",
    }
    return cat_property_type[value]


def remove_accents(text, method="unicode"):

    if method == "unicode":
        return "".join(
            c
            for c in unicodedata.normalize("NFKD", text)
            if not unicodedata.combining(c)
        )
    elif method == "ascii":
        return (
            unicodedata.normalize("NFKD", text)
            .encode("ascii", errors="ignore")
            .decode("ascii")
        )
    else:
        msg = REMOVE_ERROR_MSG.format(method)
        raise ValueError(msg)


def launch_webdriver():
    browser = os.getenv('BROWSER', 'Chrome')

    executable_path = os.path.join(
        CRAWLERS_PATH, os.getenv('EXECUTABLE_PATH', 'driver/chromedriver')
    )

    headless = os.getenv('HEADLESS', True)

    window_maximazed = os.getenv('WINDOW', False)

    options = getattr(webdriver, f"{browser}Options")()

    if eval(headless):
        options.add_argument(argument="-headless")

    if eval(window_maximazed):
        options.add_argument("--start-maximized")

    return getattr(webdriver, browser)(executable_path=executable_path, options=options)


def create_directory(data_directory="./data"):
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
