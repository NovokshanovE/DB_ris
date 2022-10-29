import os
from flask import Blueprint, request, render_template, current_app
from db_work import select
from sql_provider import SQLProvider
from access import group_required
blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
@group_required
def queries():
    if request.method == 'GET':
        return "#1"
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return "запрос1"
        else:
            return "Repeat input"

@blueprint_query.route('/queries1', methods=['GET', 'POST'])
@group_required
def queries1():
    if request.method == 'GET':
        return "#2"
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return "запрос2"
        else:
            return "Repeat input"


