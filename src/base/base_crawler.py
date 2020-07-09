# Built-in libraries
from dataclasses import dataclass, field
from typing import Any
import time
import requests

# Third-party libraries
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from flask import current_app

# Modules
from .base_functions import (
    catalogue_operation,
    catalogue_property_type,
    catalogue_website,
    launch_webdriver,
    remove_accents,
)

from .constants import (
    NO_CONTENT,
    TEXT_BOX,
    SUGGESTIONS,
    LUO_API,
)


@dataclass
class BaseCrawler:
    """
    Parameters:
        operation: for-sale, for-rent, etc.
        property_type: House, Department, development, etc.
        neighborhood: Suburb.
        state: CDMX, Veracruz, Chiapas and so on.
        cat_website: Webiste transformed according to a catolgue
        cat_operation: Operation transformed according to a catolgue
        cat_website: Property_type transformed according to a catolgue
        data: Dict with all predetermined keys to scrape the web page.
        driver: Chromedriver by default.
        municipality: "coyoacán", "benito-juárez" and so on.
        results: list of dictionaries of buildings' data.
        urls: list of all urls fetched for the whole search.
    """

    operation: str
    property_type: str
    state: str
    neighborhood: str
    municipality: str
    website: str
    cat_website: str = field(default_factory=str)
    cat_operation: str = field(default_factory=str)
    cat_property_type: str = field(default_factory=str)
    data: dict = field(default_factory=dict)
    driver: Any = field(default_factory=launch_webdriver)
    results: list = field(default_factory=list)
    urls: list = field(default_factory=list)

    def wait(self, html_element, locator, time=5):
        """Wait to load a element of a page."""

        by = getattr(By, locator)

        try:
            WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located((by, html_element))
            )

        # Siempre poner la excepcion especifica
        except TimeoutException:
            return False

        return True

    # Regresa un error, se tiene que poner dentro de un try, except.
    def find(self, html_element, locator):
        """Replace large syntaxis to find one element."""

        by = getattr(By, locator)
        return self.driver.find_element(by, html_element)

    def find_all(self, html_element, locator):
        """Replace large syntaxis to find many elements."""
        by_locator = getattr(By, locator)
        return self.driver.find_elements(by_locator, html_element)

    def catalogues(self):
        """Tranform crawler features to catalogue options."""

        self.cat_website = catalogue_website(self.website)
        self.cat_operation = catalogue_operation(self.operation)
        self.cat_property_type = catalogue_property_type(self.property_type)

    # por esto, se deben de atomizar bien las tareas de los crawlers.
    def debug_mode(self, url, method):
        """To speed up the proccess of debug crawlers errors."""

        self.driver.get(url)
        getattr(self, method)(url)

    def validate_content(self):
        """Analyze whether website returns results to extract information."""

        html_element = self.wait(**NO_CONTENT[self.website])

        if html_element:
            raise NoSuchElementException('Not buildings are current avalaible')

    def save(self):
        """Send data to API."""
        if self.results:
            response = requests.post(url=f"{LUO_API}data/", json=self.results)

            if response.ok:
                # current_app.logger.info("Data sent")
                print('data sent')
                self.results = []

            return response

    def match_address(self):
        """Extracting all the available municipality."""

        # Indicates whether the neighborhood was found
        match_found = False
        state_list = ['cdmx', 'df', 'distrito federal', 'ciudad de mexico']

        suggestions = self.find_all(**SUGGESTIONS[self.website])

        search_1 = [self.municipality, self.neighborhood]

        options = [remove_accents(opt.text.lower()) for opt in suggestions]

        for idx, opt in enumerate(options):
            if all(elem in opt for elem in search_1) and any(
                variation in opt for variation in state_list
            ):
                suggestions[idx].click()
                match_found = True
                break

            elif all(elem in opt for elem in search_1):
                suggestions[idx].click()
                match_found = True
                break

        if not match_found:
            for idx, opt in enumerate(options):
                if self.neighborhood in opt and any(
                    variation in opt for variation in state_list
                ):
                    suggestions[idx].click()
                    match_found = True
                    break

        return match_found

    def select_address(self):
        """Main method for select address."""

        self.state = remove_accents(self.state)
        self.municipality = remove_accents(self.municipality).strip()
        self.neighborhood = remove_accents(self.neighborhood).strip()

        self.wait(**TEXT_BOX[self.website])

        trouble_websites = ['inmuebles24', 'propiedades']

        attemps = 1

        if self.website in trouble_websites:
            loops = 10

        else:
            loops = 3

        result = None

        while attemps < loops:

            text_box = self.find(**TEXT_BOX[self.website])
            text_box.clear()
            text_box.send_keys(self.neighborhood)

            suggestions = self.wait(**SUGGESTIONS[self.website], time=3)

            if suggestions:
                # wait until suggestions load properly (DO NOT REMOVE!)
                time.sleep(3)
                result = self.match_address()

                if result:
                    break

            for i in range(len(self.neighborhood)):
                text_box.send_keys(Keys.BACKSPACE)

            attemps += 1

        if not result:
            raise NoSuchElementException("Neighborhood doesn't found on website")

    def validate_geolocalization(self):
        if not self.data["address"]["latitude"] or not self.data["address"]["longitude"]:
            return False

        else:
            return True
