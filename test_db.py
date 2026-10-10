from database import get_connection

print("Testing MySQL connection...")

try:
    connection = get_connection()
    print("✅ MySQL database connected successfully!")
    connection.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)