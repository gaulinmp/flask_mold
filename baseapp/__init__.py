# -*- coding: utf-8 -*-
import logging

from flask import Flask, request, render_template
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
    pages.blueprint.extra_init(app)
    app.register_blueprint(user.views.blueprint)

    app.logger.setLevel(logging.WARNING)

    app.error_handler_spec[None][404] = err_404
    app.error_handler_spec[None][500] = err_500

    return app

# This is clunky!!!
def err_404(e):
    print(404,e)
    return render_template('errors/404.html')

def err_500(e):
    print(500,e)
    return render_template('errors/500.html')
