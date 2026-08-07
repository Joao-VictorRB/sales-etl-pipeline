from mysql.connector import Error
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

def con():

    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("Connected successfully to the database")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    return connection


def closeDB(connection,cursor):
       if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("\nMySQL connection closed.")

