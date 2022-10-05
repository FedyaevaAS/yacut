import random
import string

from flask import flash, redirect, render_template, request
from urllib.parse import urljoin

from . import app, db
from .forms import URLForm
from .models import URL_map


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_URL = ''.join(random.choices(letters_and_digits, k=6))
    return short_URL


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    request_URL = request.url
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short = form.custom_id.data
    if short:
        if URL_map.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!', 'error-message')
            return render_template('index.html', form=form)
    else:
        short = get_unique_short_id()
        while URL_map.query.filter_by(short=short).first():
            short = get_unique_short_id()
    url_map = URL_map(
        original=form.original_link.data,
        short=short
    )
    db.session.add(url_map)
    db.session.commit()
    short_URL = urljoin(request_URL, short)
    flash(f'{short_URL}', 'short_link-message')
    return render_template('index.html', form=form)


@app.route('/<string:short_URL>')
def redirect_view(short_URL):
    original = URL_map.query.filter_by(short=short_URL).first_or_404().original
    return redirect(original)
