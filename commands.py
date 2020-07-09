# Built-in libraries
import pickle
import click

# Third-party libraries
from flask import Blueprint, current_app

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

# Modules
from src.crawlers.lamudi import LaMudi

from src.base.constants import MEMORY_PATH

crawlers = Blueprint('crawlers', __name__)


PAGES = {
    "lamudi": LaMudi,
}

Exceptions = (NoSuchElementException,
              StaleElementReferenceException,
              TimeoutException,
              ConnectionError,
              ElementClickInterceptedException)


@crawlers.cli.command('start')
@click.argument('page')
def start(page):
    """ Start crawler. """

    current_app.logger.info(f"INIT - Process for page {page}")

    with open(MEMORY_PATH + f'colonias-{page}.pickle', 'rb') as pickle_file:
        colonias = pickle.load(pickle_file)

    for idx, colonia in enumerate(colonias):
        current_app.logger.info(f"GET data for {colonia}")
        neighborhood = colonia.split(":::::")[0].lower()
        municipality = colonia.split(":::::")[1].lower()

        crawler = PAGES[page](operation='venta'.lower(),
                              property_type='casa'.lower(),
                              state='Distrito Federal'.lower(),
                              website=page,
                              neighborhood=neighborhood,
                              municipality=municipality)

        try:
            crawler.main()

        except Exceptions as error:
            current_app.logger.error(f"""Failed process for {page} with data {colonia} -
                                     {str(error)} and url: {crawler.driver.current_url}""")
            continue

        finally:
            crawler.driver.quit()
            # colonias.pop(idx)

            # with open(MEMORY_PATH + f'colonias-{page}.pickle', 'wb') as pickle_file:
            #   pickle.dump(colonias, pickle_file)

    return {"status": "OK"}
