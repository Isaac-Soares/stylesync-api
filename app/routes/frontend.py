from flask import Blueprint, render_template

# Criamos um "módulo" chamado frontend.
# O url_prefix='/view' significa que todas essas telas só serão acessadas
# se o usuário digitar /view na URL (ex: localhost:5000/view/login)
frontend_bp = Blueprint('frontend', __name__, url_prefix='/view')

@frontend_bp.route('/login', methods=['GET'])
def login_view():
    # Isso vai procurar o arquivo 'login.html' dentro da pasta 'templates/'
    return render_template('login.html')

@frontend_bp.route('/dashboard', methods=['GET'])
def dashboard_view():
    return render_template('dashboard.html')

@frontend_bp.route('/products', methods=['GET'])
def products_list_view():
    return render_template('products/list.html')

@frontend_bp.route('/products/new', methods=['GET'])
def products_create_view():
    return render_template('products/create.html')

@frontend_bp.route('/product/edit/<string:product_id>', methods=['GET'])
def products_edit_view(product_id):
    # Passamos o ID pela URL para o arquivo HTML saber qual produto editar
    return render_template('products/edit.html', product_id=product_id)

@frontend_bp.route('/sales/upload', methods=['GET'])
def sales_upload_view():
    return render_template('sales/upload.html')