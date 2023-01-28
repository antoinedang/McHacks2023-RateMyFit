#!/usr/bin/env python
from os import path, environ
import logging
import sys

from flask import Flask
import settings

from blueprints.mainpage import fit_api
from blueprints.client import client_api

app = Flask(__name__)

def construct_app():
    app_dir = path.dirname(path.realpath(__file__))
    app_name = path.basename(app_dir)

    app = Flask(app_name, root_path=app_dir)


    app.register_blueprint(fit_api)
    app.register_blueprint(client_api)

    app.config.from_object('settings')

    # Logging
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(app.config.get('LOG_LEVEL', logging.INFO))
    app.debug = True

    return app


app = construct_app()

if __name__ == '__main__':
    environ['FLASK_DEBUG'] = 'development'
    config = app.config
    app.run(debug=True,host='0.0.0.0', port=config['APP_PORT'])