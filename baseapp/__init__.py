# -*- coding: utf-8 -*-
import logging

from flask import Flask, request
from flask_wtf.csrf import CsrfProtect

from .controllers import pages, user
from .extensions import all_extensions


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    CsrfProtect(app)

    for ext in all_extensions:
        ext.init_app(app)

    app.register_blueprint(pages.blueprint)
    app.register_blueprint(user.views.blueprint)

    app.logger.setLevel(logging.WARNING)

    return app
