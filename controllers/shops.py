from flask import jsonify

from dbConnection import db


def create_shop_by_user_id(shop_name, description, user_id):
    try:
        # db connection
        connection = db.create_connection()
        cursor = connection.cursor()
        user_is_admin = "SELECT * FROM users WHERE id = %s"
        cursor.execute(user_is_admin, (user_id,))
        result = cursor.fetchone()
        if result[4] == 1:
            existing_name_query = "SELECT name FROM shops WHERE name = %s"
            cursor.execute(existing_name_query, (shop_name,))
            existing_shop = cursor.fetchone()
            if bool(existing_shop):
                cursor.close()
                connection.close()
                return (
                    jsonify(
                        {"message": "This name is already used, try some other name"}
                    ),
                    400,
                )
            already_shop_owner = "SELECT * FROM shops WHERE owner = %s"
            cursor.execute(already_shop_owner, (user_id,))
            row = cursor.fetchone()
            if not bool(row):
                create_query = (
                    "INSERT INTO shops (name, description, owner) VALUES (%s, %s, %s)"
                )
                cursor.execute(create_query, (shop_name, description, user_id))

                connection.commit()

                new_shop_id = cursor.lastrowid

                cursor.close()
                connection.close()

                return (
                    jsonify(
                        {"message": "Shop Created Successfully", "shop_id": new_shop_id}
                    ),
                    201,
                )
            else:
                return jsonify({"message": "You already own a shop !"}), 404
        else:
            cursor.close()
            connection.close()
            return jsonify({"message": "You are not Authorized"})
    except Exception as err:
        return jsonify({"message": str(err)})


def get_all_shops():
    try:
        connection = db.create_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM shops"
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify({"message": "Found shops", "shops": result})
    except KeyError as err:
        return jsonfiy({"message": str(err)})


def update_shop_by_ids(new_name, new_description, shop_id, user_id):
    try:
        connection = db.create_connection()
        cursor = connection.cursor()
        # check if the shop exists
        check_shop_query = "SELECT * FROM shops WHERE id = %s"
        cursor.execute(check_shop_query, (shop_id,))
        shop = cursor.fetchone()
        print(shop)
        if not shop:
            cursor.close()
            connection.close()
            return jsonify({"error": "Shop not found"}), 404
        if shop[3] != user_id:
            cursor.close()
            connection.close()
            return jsonify({"message": "You are not the owner"}), 405

        update_query = "UPDATE shops SET name = %s, description = %s WHERE id = %s"
        cursor.execute(update_query, (new_name, new_description, shop_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Shop Updated successfully"})
    except Exception as err:
        return jsonify({"message": str(err)}), 400


def delete_shop_by_id(shop_id, user_id):
    try:
        connection = db.create_connection()
        cursor = connection.cursor()
        # Check if the shop with the given ID exists
        check_shop_query = "SELECT * FROM shops WHERE id = %s"
        cursor.execute(check_shop_query, (shop_id,))
        shop = cursor.fetchone()
        print(shop)
        if not shop:
            cursor.close()
            connection.close()
            return jsonify({"error": "Shop not found"}), 404
        if shop[3] != user_id:
            cursor.close()
            connection.close()
            return jsonify({"message": "You are not the owner"}), 405
        # delete the shop with that id
        query = "DELETE FROM shops WHERE id = %s"
        cursor.execute(query, (shop_id,))
        connection.commit()

        cursor.close()
        connection.close()
        return jsonify({"message": "Shop Deleted successfully..."}), 200
    except Exception as err:
        return jsonify({"message": str(err)}), 400
