import pymssql

# Connect to master database
conn = pymssql.connect(
    server='127.0.0.1',
    user='sa',
    password='@Bina0608',
    database='master',
    autocommit=True  # Important for DDL statements
)

cursor = conn.cursor()

# Drop database if exists
try:
    # Kill all connections to PlatformDB first
    cursor.execute("""
        ALTER DATABASE PlatformDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE
    """)
    print("Set database to single user mode")
    
    cursor.execute("DROP DATABASE PlatformDB")
    print("Database PlatformDB dropped successfully")
except Exception as e:
    print(f"Drop failed (maybe DB doesn't exist): {e}")

# Create new database
cursor.execute("CREATE DATABASE PlatformDB")
print("Database PlatformDB created successfully")

conn.close()
