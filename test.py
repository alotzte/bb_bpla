import psycopg2

try:
    connection = psycopg2.connect(
        host="134.122.58.32",
        port="16543",
        user="postgres",
        password="password",
        database="postgres"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record)

finally:
    connection.close()
