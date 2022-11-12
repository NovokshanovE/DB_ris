import os.path
from flask import Blueprint, request, render_template, current_app, redirect, url_for
from access import login_required, group_required
from db_work import select, select_dict, insert
from sql_provider import SQLProvider

blueprint_report = Blueprint('bp_edit', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_edit.route('/',methods=['GET', "POST"])
def show_all_products():
    _sql = provider.get('all_products.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    return render_template('all_product.html', products = products)


@blueprint_edit.route('/update',methods=['GET', "POST"])
def show_all_products():
    action = request.form.get('action')
    prod_id = request.form.get('prod_id')

    if action == 'edit_prod':

        _sql = provider.get('get_product_by_id.sql', prod_id=prod_id)
        product = select_dict(current_app.config['db_config'], _sql)[0]
        return render_template('all_product.html', product = product)
    if action == 'del_prod':
        message = del_prod(prod_id)
        return render_template('update_ok.html', message=message)
    if action == 'update_prod':
        message = update_prod(prod_id)
        return render_template('update_ok.html', message=message)

def del_prod(prod_id):
    message = "del ok"
    return message


@blueprint_edit.route('/insert_prod', methods=['GET'])
def insert_prod(prod_id):
    _sql = provider.get('get_product_by_id.sql', prod_id=prod_id)
    product = select_dict(current_app.config['db_config'], _sql)[0]
    return render_template('product_update.html', product=product)




@blueprint_edit.route('/insert_prod', methods=["POST"])
def insert_product():
    new_name = request.form.get('prod_name')
    new_price = request.form.get('prod_price')
    if new_price and new_name:

        _sql = provider.get('insert_prod.sql', new_name=new_name, new_price=new_price)
        if (insert(current_app.config['db_config'], _sql) == 1)
            return redirect(url_for('bp_edit.show_all_products'))

