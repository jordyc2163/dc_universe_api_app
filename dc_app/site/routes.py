from re import template
from flask import Blueprint, render_template
from flask_login import login_required
from dc_app.forms import SearchCharacterForm

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    form = SearchCharacterForm()
    return render_template('index.html', form=form)

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/about')
def about():
    return render_template('about.html')
