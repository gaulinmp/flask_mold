# -*- coding: utf-8 -*-
from flask import render_template, Blueprint, current_app

blueprint = Blueprint('baseapp', __name__)


################
#### routes ####
################


@blueprint.route('/')
def home():
    return render_template('layouts/skeleton.html')
