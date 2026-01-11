import pymssql
import time

def create_database():
    retries = 5
    while retries > 0:
        try:
            print("Connecting to SQL Server...")
            conn = pymssql.connect(server='127.0.0.1', user='sa', password='@Bina0608', database='master')
            conn.autocommit(True)
            cursor = conn.cursor()
            try:
                cursor.execute("CREATE DATABASE PlatformDB")
                print("Database PlatformDB created successfully.")
            except Exception as e:
                if "already exists" in str(e):
                    print("Database PlatformDB already exists.")
                else:
                    print(f"Error creating database: {e}")
            conn.close()
            return
        except Exception as e:
            print(f"Connection failed: {e}")
            retries -= 1
            time.sleep(5)
    
    print("Failed to connect to SQL Server after multiple attempts.")

if __name__ == "__main__":
    create_database()
