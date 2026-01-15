import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="Aditya@123")
cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS drishti_db")
cursor.execute("CREATE DATABASE drishti_db")
print("Database drishti_db reset successfully.")
db.close()
