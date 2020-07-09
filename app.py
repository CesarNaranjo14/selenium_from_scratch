""" Crawlers API """
# Third-party libraries
import os

from flask import Flask
from commands import crawlers
from create_pickles import create_pickles


app = Flask(__name__)

app.register_blueprint(crawlers)
app.register_blueprint(create_pickles)


if __name__ == '__main__':
    port = 3031
    host = "localhost"
    app.run(debug=os.environ.get('DEBUG', False), host=host, port=port)
