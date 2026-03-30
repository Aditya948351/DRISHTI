
import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

def check_db_connection():
    db_conn = connections['default']
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT 1;")
        row = cursor.fetchone()
        print(f"Database query successful! Result: {row}")
        return True
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    if check_db_connection():
        sys.exit(0)
    else:
        sys.exit(1)
