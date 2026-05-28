from database.engine import get_connection

conn = get_connection()         #needs UPDATE -------------------------------------------------

if conn:
    print("Connected successfully")
    conn.close()
else:
    print("Connection failed")

