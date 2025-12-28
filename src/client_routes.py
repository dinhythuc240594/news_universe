
"""
client router - define routes for client
"""

from flask import Blueprint, render_template, request, jsonify, abort, make_response

import base
import client_controller


# Create Blueprint for client with url_prefix is empty to redirect route
# and template_folder for html files in folder client
client_bp = Blueprint('client', __name__, 
                     url_prefix='',
                     template_folder='templates')


class Home(base.BaseView):

    def get(self):
        return 'Home'


client_bp.add_url_rule('/home', 'home', Home.as_view('home'))
