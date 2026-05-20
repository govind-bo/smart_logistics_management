from src.database.connection import get_connection

conn = get_connection()

if conn:
    print("Connected successfully")
    conn.close()
else:
    print("Connection failed")

