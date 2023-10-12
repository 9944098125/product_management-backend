from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from dbConnection import db


def register_user(name, email, password, is_admin):
    try:
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        connection = db.create_connection()
        # create a connection cursor
        cursor = connection.cursor()
        if not connection:
            return {"message": "Database connection Failed !"}
        # check is a user with same email exists
        same_email = "SELECT * FROM users WHERE email = %s"
        cursor.execute(same_email, (email,))
        result = cursor.fetchone()
        if result:
            return jsonify({"message": "User with this email already exists !"}), 404

        query = "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, hashed_password, is_admin))
        connection.commit()
        return jsonify({"message": "User Created Successfully..."})
    except Exception as err:
        return jsonify({"error": str(err)}), 404


def login_user(email, password):
    try:
        connection = db.create_connection()

        if not connection:
            return jsonify({"message": "Database Connection Failed"})

        query = "SELECT * FROM users WHERE email = %s"
        cursor = connection.cursor()
        cursor.execute(query, (email,))

        user_data = cursor.fetchone()
        print(user_data)

        if not user_data:
            cursor.close()
            connection.close()
            return jsonify({"message": "User not found !"}), 404

        if check_password_hash(user_data[3], password):
            cursor.close()
            connection.close()
            return (
                jsonify(
                    {
                        "message": "Login Success",
                        "user": {
                            "id": user_data[0],
                            "name": user_data[1],
                            "email": user_data[2],
                            "is_admin": user_data[4],
                        },
                    }
                ),
                200,
            )
        else:
            cursor.close()
            connection.close()
            return jsonify({"message": "Invalid Password !"}), 405
    except Exception as err:
        return jsonify({"message": str(err)})


def get_all_users():
    connection = db.create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    return {"message": "Found Users", "users": users}


def delete_all_users():
    connection = db.create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM users"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Deleted All the Users"}
