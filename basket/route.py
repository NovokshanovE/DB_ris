import os.path
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from access import login_required, group_required
from db_work import select, select_dict
from sql_provider import SQLProvider

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_order.route('/',methods=['GET', "POST"])
def order_index():
    db_config= current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)

        add_to_basket(prod_id, items)
        return redirect(url_for('bp_order.order_index'))
