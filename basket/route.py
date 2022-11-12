import os.path
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from access import login_required, group_required, session
from db_work import select, select_dict
from sql_provider import SQLProvider
import db_context_manager

blueprint_basket = Blueprint('bp_basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_basket.route('/',methods=['GET', "POST"])
def order_index():
    db_config= current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket_items=basket_items)
    else:
        prod_id = request.form['prod_id']
        sql = provider.get('select_items.sql', prod_id=prod_id)
        items = select_dict(db_config, sql)

        add_to_basket(prod_id, items)
        return redirect(url_for('bp_order.order_index'))


def add_to_basket(prod_id: str, items: dict):
    #item_description = [item for item in items if str(item['prod_id'])]
    #print('item_description before = ', item_description)
    #item_description = item_description[0]

    curr_basket = session.get('basket', {})
    if prod_id in curr_basket:
        curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount']+1
    else:
        curr_basket[prod_id]['amount'] = {
            'prod_name': items['prod_name'],
            'prod_price': items['prod_price'],
            'amount': 1


        }
        session['basket'] = curr_basket
        session.permanent = True
    return True

@blueprint_basket.route('/save_order',methods=['GET', "POST"])
def save_order():
    user_id = session.get('user_id')
    current_basket = session.get('basket', {})
    order_id = save_order_list(current_app.config['db_config'], user_id, current_basket)
    if order_id:
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id)
    else:
        return "Подумай над своим поведением"


def save_order_list(dbconfig: dict, user_id: int, current_basket: dict):
    with DBContextManager(dbconfig) as cursor:
