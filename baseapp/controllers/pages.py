# -*- coding: utf-8 -*-
from flask import render_template, Blueprint

blueprint = Blueprint('baseapp', __name__,
                      static_folder='../static',
                      template_folder='../templates')

################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route('/')
def home():
    return render_template('layouts/skeleton.html')

# Add more routes here. Or copy this file and make a new blueprint.

################################################################################
####           Add to App Context Manager                                   ####
################################################################################
def extra_init(app):
    """Extra blueprint initialization that requires application context."""
    if 'header_links' not in app.jinja_env.globals:
        app.jinja_env.globals['header_links'] = []
    # Add links to 'header_links' var in jinja globals. This allows header_links
    # to be read by all templates in the app instead of just this blueprint.
    app.jinja_env.globals['header_links'].extend([("Home", 'baseapp.home')])
# Tack it on to blueprint for easy access in app's __init__.py
blueprint.extra_init = extra_init
