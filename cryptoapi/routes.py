from flask import abort, jsonify, request, url_for

from cryptoapi import app
from .models import Crypto


# Utility function for URL building.
def build_url(view_url):
    # hack for deploying to lambda
    view_url = view_url.replace('dev/', '')
    return '{0}{1}'.format(app.config['ROOT_URL'], view_url)


# Build crypto data dict with detail url
def single_crypto_response(crypto):
    res = crypto.root_to_dict()
    res['_detail'] = build_url(url_for('get_crypto', id=crypto.id))
    return res


@app.route('/')
def index():
    return jsonify({
        'repo': 'https://github.com/sjbitcode/crypto495',
        'endpoints': {
            'Crypto Search': {
                'url': '{}/cryptos'.format(app.config['ROOT_URL']),
                'description': 'Get list of 500 cryptos',
                'query parameters': {
                    'filter': '(str) search term to search against name and slug fields'
                },
                'response': {
                    'count': 'Total results per page',
                    'total': 'Total results returned from query',
                    'page': 'Current page',
                    'prev_page': 'Url to previous page if any',
                    'next_page': 'Url to next page if any',
                    'data': 'Results of query returned as list of objects'
                }
            },
            'Crypto Detail': {
                'url': '{}/cryptos/{{id}}'.format(app.config['ROOT_URL']),
                'description': 'Get details of crypto by a given id',
                'query parameters': {},
                'response': {
                    'data': 'Full details of given crypto as an object'
                }
            },
            'Token List': {
                'url': '{}/cryptos/{{id}}/tokens'.format(app.config['ROOT_URL']),
                'description': 'Get all cryptos that are tokens of a single crypto by a given id',
                'query parameters': {},
                'response': {
                    'total': 'Total results returned',
                    'data': 'Results of tokens returned as list of objects'
                }
            },
            'Category Search': {
                'url': '{}/categories'.format(app.config['ROOT_URL']),
                'description': 'Get all cryptos categorized by coin or token',
                'query parameters': {
                    'type': '(str) "coin" OR "token" get only one categorization'
                },
                'response': {
                    'data': 'Results of query returned as list of objects categorized under "coins" and/or "tokens" keys'
                }
            }

        }
    })


@app.route('/cryptos', methods=['GET'])
def get_cryptos():
    page = request.args.get('page', 1, type=int)
    cryptos = Crypto.query

    if 'filter' in request.args:
        filter = request.args.get('filter', '', type=str)
        cryptos = Crypto.query.filter(
            Crypto.name.ilike(r"%{}%".format(filter)),
            Crypto.slug.ilike(r"%{}%".format(filter))
        )

    # order and paginate query
    cryptos = cryptos.order_by(Crypto.name).paginate(
        page, app.config['PAGINATION_LIMIT'], error_out=False)

    return jsonify({
        'count': len(cryptos.items),
        'total': cryptos.total,
        'page': cryptos.page,
        'prev_page': build_url(url_for('get_cryptos', page=cryptos.prev_num)) if cryptos.has_prev else None,
        'next_page': build_url(url_for('get_cryptos', page=cryptos.next_num)) if cryptos.has_next else None,
        'data': [
            single_crypto_response(crypto) for crypto in cryptos.items
        ]
    })


@app.route('/cryptos/<id>', methods=['GET'])
def get_crypto(id):
    fields = [
        'name', 'symbol', 'slug', 
        'created', 'website', 'repo', 
        'description', 'platform', 'category', 'logo'
    ]

    # Get crypto object
    crypto = Crypto.query.filter_by(id=id).first_or_404()
    res = {
        'data': {}
    }

    print(request.args)
    if 'fields' in request.args:
        query_fields = request.args.get('fields', '', type=str).lower().split(',')

        # Validate query fields against valid model fields
        if set(query_fields).issubset(fields):
            res['data'] = {key: val for (key, val) in crypto.to_dict().items() if key in query_fields}
            return jsonify(res)
        else:
            abort(400)
    else:
        res['data'] = crypto.to_dict()
        return jsonify(res)


@app.route('/cryptos/<id>/tokens', methods=['GET'])
def get_tokens(id):
    platform = Crypto.query.filter_by(id=id).first_or_404()
    token_list = Crypto.query.filter_by(platform=platform.name).all()
    return jsonify({
        'total': len(token_list),
        'data': [
            single_crypto_response(crypto) for crypto in token_list
        ]
    })


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = ['coin', 'token']
    res = {
        'data': {}
    }

    if 'type' in request.args:
        query_type = request.args.get('type', '', type=str)

        if query_type not in categories:
            abort(400)

        queryset = Crypto.query.filter_by(category=query_type).all()

        res['data'][f'{query_type}s'] = {
            'total': len(queryset),
            'list': [single_crypto_response(crypto) for crypto in queryset]
        }
    else:
        for coin_type in categories:
            queryset = Crypto.query.filter_by(category=coin_type).all()
            res['data'][f'{coin_type}s'] = {
                'total': len(queryset),
                'list': [single_crypto_response(crypto) for crypto in queryset]
            }
    return jsonify(res)
