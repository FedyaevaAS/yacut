import re

from flask import jsonify, request
from urllib.parse import urljoin

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    request_URL = request.url_root
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    elif 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    condition = ('custom_id' in data and
                 data['custom_id'] is not None and
                 len(data['custom_id']) > 0)
    if condition:
        custom_id = data['custom_id']
        condition_first = (len(custom_id) > 16 or not
                           re.match(r'^[a-zA-Z0-9]+$', custom_id))
        condition_second = URL_map.query.filter_by(
            short=custom_id
        ).first() is not None
        if condition_first:
            raise InvalidAPIUsage('Указано недопустимое '
                                  'имя для короткой ссылки')
        elif condition_second:
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    else:
        custom_id = get_unique_short_id()
    original = data['url']
    url = URL_map(
        original=original,
        short=custom_id
    )
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {'url': original, 'short_link': urljoin(request_URL, custom_id)}
    ), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
