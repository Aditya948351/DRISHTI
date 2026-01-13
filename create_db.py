import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    # Get database config from environment or use defaults (matching settings.py)
    db_name = os.environ.get('DB_NAME', 'drishti_db')
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'Aditya@123')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '3306')

    print(f"Connecting to MySQL at {db_host}:{db_port} as {db_user}...")

    try:
        # Connect to MySQL server
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port
        )

        cursor = mydb.cursor()
        
        # Check if database exists
        cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
        result = cursor.fetchone()

        if result:
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Database '{db_name}' does not exist. Creating...")
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully!")

        cursor.close()
        mydb.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Please ensure MySQL is running and the credentials are correct.")

if __name__ == "__main__":
    create_database()
