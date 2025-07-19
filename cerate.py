import psycopg2
from psycopg2 import sql

# Configuration
db_name = "hagg"
user = "postgres"
password = "postgres"
host = "127.0.0.1"
port = "5432"

# Connect to the default 'postgres' database
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True  # Needed to CREATE DATABASE
    cur = conn.cursor()

    # SQL command to create database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name)
    ))

    print(f"Database '{db_name}' created successfully.")

    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Error creating database:", e)
