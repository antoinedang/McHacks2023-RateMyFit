#!/usr/bin/env python
from os import path

from flask import Flask
import settings

from blueprints.mainpage import fit_api

app = Flask(__name__)

def construct_app():
    app_dir = path.dirname(path.realpath(__file__))
    app_name = path.basename(app_dir)

    app = Flask(app_name, root_path=app_dir, static_url_path='/static')


    app.register_blueprint(fit_api)

    return app


app = construct_app()

if __name__ == '__main__':
    config = app
    app.run(host='0.0.0.0', port=5002)