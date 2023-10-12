from flask import Flask
from flask_cors import CORS

# importing Flask instance & CORS
from dbConnection import db

# importing database connection
from routes.auth import auth_blueprint
from routes.shops import shops_blueprint
from routes.products import products_blueprint

# importing blueprints from routes

# let's take app as an instance of Flask in which this file (__name) is executed
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# users registration, login and get all users
app.register_blueprint(auth_blueprint, url_prefix="/api/auth")

# crud operations with shops
app.register_blueprint(shops_blueprint, url_prefix="/api/shops")

# crud operations with products
app.register_blueprint(products_blueprint, url_prefix="/api/products")

if __name__ == "__main__":
    db.create_connection()
    app.run(debug=True)
