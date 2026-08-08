from  flask import Blueprint, jsonify, request, current_app, redirect, url_for
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import *
from app.models.sale import Sale
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt
import csv
import os
import io

main_bp = Blueprint('main', __name__)

# RF: O Sistema deve permitir que um usuario se altentique para obter um token de acesso
@main_bp.route("/login", methods=["POST"])
def get_login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    except Exception as e:
        return jsonify({"error": "Erro durante a requisicao de login."}), 500

    if user_data.username == "admin" and user_data.password == "supersecret":
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({"access_token": token}), 200
    
    return jsonify({"message": "Usuario ou senha incorretos."}), 401

   



# RF: O Sistema deve permitir listagem de todos os produtos cadastrados no sistema
@main_bp.route("/products", methods=["GET"])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
    return jsonify(products_list)


# RF: O Sistema deve permitir a cricao de novos produtos no sistema
@main_bp.route("/products", methods=["POST"])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = db.products.insert_one(product.model_dump(by_alias=True, exclude_none=True))

    return jsonify({"message": "Criando um novo produto", "id" : str(result.inserted_id)}), 201


# RF: O Sistema deve permitir a vizualizacao de detalhes de um produto especifico
@main_bp.route("/product/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):

    try:
        oid = ObjectId(product_id)  # Validate if product_id is a valid ObjectId

    except Exception as e:
        return jsonify({"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"})
    
    product = db.products.find_one({"_id": oid})

    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)  # Convert ObjectId to string
        return jsonify(product_model)
    else:
        return jsonify({"error": f"Produto com id {product_id} nao encontrado."}), 404
    


# RF: O Sistema deve permitir a atualizacao de um produto especifico existente no sistema
@main_bp.route("/product/<string:product_id>", methods=["PUT"])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)  # Validate if product_id is a valid ObjectId
        update_data = UpdateProduct(**request.get_json())  # Validate the incoming data against UpdateProduct model

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    update_result = db.products.update_one({"_id": oid}, {"$set": update_data.model_dump(exclude_unset=True)})

    if update_result.matched_count == 0:
        return jsonify({"error": f"Produto com id {product_id} nao encontrado."}), 404
    
    update_product = db.products.find_one({"_id": oid})
    return jsonify(ProductDBModel(**update_product).model_dump(by_alias=True, exclude_none=True)), 200


# RF: O Sistema deve permitir a delacao de um produto especifico existente no sistema
@main_bp.route("/product/<string:product_id>", methods=["DELETE"])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)  # Validate if product_id is a valid ObjectId
    except Exception as e:
        return jsonify({"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"})
    
    delete_product = db.products.delete_one({"_id": oid})

    if delete_product.deleted_count == 0:
        return jsonify({"error": f"Produto com id {product_id} nao encontrado."}), 404

    return "", 204


# RF: O Sistema deve permitir a importacao de produtos a partir de um arquivo
@main_bp.route("/sales/upload", methods=["POST"])
@token_required
def upload_sales(token):
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]

    if file.filename == "":
         return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    if file and file.filename.endswith(".csv"):
        csv_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(csv_stream)

        sales_to_insert = []
        error = []

        for row_num, row in enumerate(csv_reader, 1):
            try:
                sale_data = Sale(**row)

                sale_dict = sale_data.model_dump()
                sale_dict["sale_date"] = datetime.combine(
                    sale_data.sale_date,
                    datetime.min.time()
                )

                sales_to_insert.append(sale_dict)

            except ValidationError as e:
                error.append(f"Linha {row_num} com dados invalidos")
            except Exception:
                error.append(f"Linha {row_num} com erro inesperado nos dados")

        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return jsonify({"error" : f"{e}"})
        return jsonify({
            "message" : "Upload realizado com sucesso",
            "vendas importadas" : len(sales_to_insert),
            "erros encontrados" : error
        }),200
                



    return jsonify({"message": "Realizando upload das vendas."})


@main_bp.route("/")
def index():
    return redirect(url_for('frontend.login_view'))



