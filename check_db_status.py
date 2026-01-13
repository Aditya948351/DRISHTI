import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME'),
        port=os.environ.get('DB_PORT')
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'django_session'")
    table = cursor.fetchone()
    if table:
        print("Table 'django_session' FOUND.")
    else:
        print("Table 'django_session' NOT FOUND.")
    
    cursor.execute("SELECT COUNT(*) FROM complaints_department")
    count = cursor.fetchone()[0]
    print(f"Departments found in DB: {count}")

    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"Total tables: {len(tables)}")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
