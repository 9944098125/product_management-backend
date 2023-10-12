from flask import jsonify

from dbConnection import db


def create_product_with_ids(shop_id, user_id, product_name, product_price):
    try:
        # Establish a database connection
        connection = db.create_connection()
        cursor = connection.cursor()

        # Check if the shop with the given ID exists
        check_shop_query = "SELECT * FROM shops WHERE id = %s"
        cursor.execute(check_shop_query, (shop_id,))
        shop = cursor.fetchone()

        if not shop:
            cursor.close()
            connection.close()
            return jsonify({"error": "Shop not found"}), 404

        # Check if the user making the request is the owner of the shop
        if shop[3] != user_id:
            cursor.close()
            connection.close()
            return jsonify({"error": "You are not the owner of this shop"}), 403

        # Create the product within the shop
        insert_product_query = (
            "INSERT INTO products (name, price, shop_id) VALUES (%s, %s, %s)"
        )
        cursor.execute(insert_product_query, (product_name, product_price, shop_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Product created successfully"})

    except Exception as err:
        return jsonify({"error": str(err)}), 500


def get_products_in_shop(shop_id):
    try:
        connection = db.create_connection()
        cursor = connection.cursor()

        get_products_query = "SELECT * FROM products WHERE shop_id = %s"
        cursor.execute(get_products_query, (shop_id,))
        result = cursor.fetchall()
        return jsonify({"message": "Found the products.", "products": result})
    except KeyError as err:
        return jsonify({"message": str(err)})


def update_product_with_ids(shop_id, user_id, product_id, product_new_name, new_price):
    try:
        connection = db.create_connection()
        cursor = connection.cursor()

        # check if the shop exists
        shop_exists = "SELECT * FROM shops WHERE id = %s"
        cursor.execute(shop_exists, (shop_id,))
        shop = cursor.fetchone()

        if not shop:
            cursor.close()
            connection.close()
            return jsonify({"message": "Shop not Found !"}), 400
        # check the owner of the shop
        if shop[3] != user_id:
            cursor.close()
            connection.close()
            return jsonify({"message": "You are not the owner !"}), 403
        # check if the product with that id exists
        product_exists = "SELECT * FROM products WHERE id = %s AND shop_id = %s"
        cursor.execute(product_exists, (product_id, shop_id))
        product = cursor.fetchone()

        # if product does not exist
        if not product:
            cursor.close()
            connection.close()
            return jsonify({"message": "Product does not exist..."}), 400
        update_query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        cursor.execute(update_query, (product_new_name, new_price, product_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Product updated successfully..."}), 200
    except Exception as err:
        return jsonify({"message": str(err)}), 403


def delete_product_with_ids(shop_id, user_id, product_id):
    try:
        connection = db.create_connection()
        cursor = connection.cursor()

        # check if shop exists
        check_shop_query = "SELECT * FROM shops WHERE id = %s"
        cursor.execute(check_shop_query, (shop_id,))
        shop = cursor.fetchone()

        if not shop:
            cursor.close()
            connection.close()

            return jsonify({"message": "shop does not exist..."}), 400
        if shop[3] != user_id:
            cursor.close()
            connection.close()
            return (
                jsonify(
                    {
                        "message": "You are not the owner of the shop containing this product..."
                    }
                ),
                400,
            )
        check_product_exists = "SELECT * FROM products WHERE id = %s"
        cursor.execute(check_product_exists, (product_id,))
        product = cursor.fetchone()

        if not product:
            cursor.close()
            connection.close()
            return jsonify({"message": "Product does not exist..."}), 403

        delete_query = "DELETE FROM products WHERE id = %s"
        cursor.execute(delete_query, (product_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": "Deleted the product successfully..."})
    except Exception as err:
        return jsonify({"message": str(err)})
