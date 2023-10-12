import mysql.connector

# importing the database connector


# create a function to export connection
def create_connection():
    # create a configuration for database connection
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Srinivas@8",
        "database": "products_management_app",
    }

    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected:
            print("Successfully Connected to database...")
            return connection
    except mysql.connector.Error as err:
        print(f"Failed connecting to database with error {err}")
        return None
