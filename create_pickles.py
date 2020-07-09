"""
DESCRIPTION
Create a set of pickle files of neighborhoods.
These files are for the use of giving the crawlers a "memory",
that is, we remove a neighborhood every time a crawler finishes
to scrap it in order to not iterate again.

HOW TO RUN
You have to run inside this directory:
    python create_pickle start
"""

# Built-in libraries
import pickle
import os

# Third-party libraries
from flask import Blueprint

# Modules
from src.base.constants import MEMORY_PATH, CRAWLERS_PATH

create_pickles = Blueprint('create_pickles', __name__)

pages = [
    "inmuebles24",
    "icasas",
    "vivanuncios",
    "propiedades",
    "lamudi",
]


@create_pickles.cli.command('start')
def pickles():
    """Create a set of pickles for every website."""

    if not os.path.exists(MEMORY_PATH):
        os.makedirs(MEMORY_PATH)

    for page in pages:
        with open(f"{CRAWLERS_PATH}colonias.txt", "r") as myfile:
            colonias = [colonia.lower().strip() for colonia in myfile]

        with open(f"{MEMORY_PATH}colonias-{page}.pickle", "wb") as pickle_file:
            pickle.dump(colonias, pickle_file)
