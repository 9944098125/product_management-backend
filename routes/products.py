from flask import request, Blueprint

from controllers.products import (
    create_product_with_ids,
    get_products_in_shop,
    update_product_with_ids,
    delete_product_with_ids,
)

products_blueprint = Blueprint("products", __name__)


# create products
@products_blueprint.route("/create/<int:shop_id>/<int:user_id>", methods=["POST"])
def create_products(shop_id, user_id):
    data = request.get_json()
    product_name = data.get("name")
    product_price = data.get("price")
    return create_product_with_ids(shop_id, user_id, product_name, product_price)


# get products with shop id
@products_blueprint.route("/<int:shop_id>", methods=["GET"])
def get_products(shop_id):
    return get_products_in_shop(shop_id)


# update a product with id
@products_blueprint.route(
    "/update/<int:shop_id>/<int:user_id>/<int:product_id>", methods=["PUT"]
)
def update_product(shop_id, user_id, product_id):
    data = request.get_json()
    product_new_name = data["name"]
    new_price = data["price"]
    return update_product_with_ids(
        shop_id, user_id, product_id, product_new_name, new_price
    )


# delete product with id
@products_blueprint.route(
    "/delete/<int:shop_id>/<int:user_id>/<int:product_id>", methods=["DELETE"]
)
def delete_product(shop_id, user_id, product_id):
    return delete_product_with_ids(shop_id, user_id, product_id)
