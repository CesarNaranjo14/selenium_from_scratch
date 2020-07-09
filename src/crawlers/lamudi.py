# Built-in libraries
import json
from dataclasses import dataclass

# Third-party libraries
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import JavascriptException

# Modules
from ..base.base_crawler import BaseCrawler
from ..base.base_functions import (
    format_data,
    catalogue_property_type
)

from ..base.page_constants import CRAWLERS_URLS


@dataclass
class LaMudi(BaseCrawler):

    def select_operation(self):
        """Define the type of operation."""

        operations = {
            'renta': 'for-rent',
            'venta': 'for-sale'
        }
        
        operation = operations[self.operation]

        self.find(f"//div[@data-value='{operation}']", "XPATH").click()

    def select_property_type(self):
        if self.property_type:
            select = Select(self.find("select", "TAG_NAME"))
            select.select_by_value(self.property_type)

    def filter_query(self):
        self.select_property_type()
        self.select_operation()
        self.select_address()

    def navigate(self):
        """Navigate untill all pages are scraped."""

        # Agregar sufijo a la url
        base_url = self.driver.current_url + "?page={}"

        URLS = "//h3[@class='ListingCell-KeyInfo-title']/a"

        # Gets the total of result pages to be iterated upon
        pages = self.find("js-pagination-dropdown", "CLASS_NAME")
        total_pages = int(pages.get_attribute("data-pagination-end"))

        for page in range(1, total_pages + 1):
            urls = self.find_all(URLS, "XPATH")
            urls = [item.get_attribute('href') for item in urls]

            self.urls.extend(urls)

            self.driver.get(base_url.format(page + 1))

    def scrape(self):
        """Fetch data of every building publication."""

        for idx, main_url in enumerate(self.urls):
            self.driver.get(main_url)

            self.get_building_features(main_url)
            # Remove url that were scraped
            self.urls.pop(idx)
        
            
            '''self.wait('/html/body/script[2]/text()', 'XPATH')
            JSON_DATA = "return JSON.stringify(dataLayer)"

            try:
                bldg_data = self.driver.execute_script(JSON_DATA)
                bldg_data = json.loads(bldg_data)[0]

                self.get_building_features(main_url, bldg_data)
            except JavascriptException:
                print(self.driver.current_url)'''

    def get_building_features(self, url, is_development=False):
        """Fetch all the building features."""

        self.data = format_data()
        # Extraer informacion de la pagina

    def building_geolocalization(self):
        # Address
        # Añadir xpath

        # Complete address with google maps information
        try:
            # location = reverse_geocode(self.data["latitude"], self.data["longitude"])
            pass

        except Exception:
            return False

    def building_amenities(self, bldg_data):
        """Amenities."""
        pass

    def main(self):

        self.driver.implicitly_wait(10)
        self.catalogues()
        self.driver.get(CRAWLERS_URLS[self.website])

        self.filter_query()
        self.validate_content()

        self.navigate()
        self.scrape()
        self.save()
