from flask import request, Blueprint

from controllers.shops import (
    create_shop_by_user_id,
    get_all_shops,
    update_shop_by_ids,
    delete_shop_by_id,
)

shops_blueprint = Blueprint("shops", __name__)


# create shop (only one shop for one admin user)
@shops_blueprint.route("/create/<int:user_id>", methods=["POST"])
def create_shop(user_id):
    data = request.get_json()
    shop_name = data["name"]
    description = data["description"]
    return create_shop_by_user_id(shop_name, description, user_id)


# get shops
@shops_blueprint.route("/", methods=["GET"])
def get_shops():
    return get_all_shops()


# update shop if user id matches owner
@shops_blueprint.route("/update/<int:shop_id>/<int:user_id>", methods=["PUT"])
def update_shop(shop_id, user_id):
    data = request.get_json()
    new_name = data.get("name")
    new_description = data.get("description")
    return update_shop_by_ids(new_name, new_description, shop_id, user_id)


# delete a shop with id
@shops_blueprint.route("/delete/<int:shop_id>/<int:user_id>", methods=["DELETE"])
def delete_shop(shop_id, user_id):
    return delete_shop_by_id(shop_id, user_id)
