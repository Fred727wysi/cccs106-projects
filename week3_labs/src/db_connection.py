import mysql.connector
from mysql.connector import Error

def connect_db():
    """
    Establishes connection to MySQL database
    Returns mysql.connector connection object
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678", 
            database="flettapp"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise e