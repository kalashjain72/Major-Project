from mysql.connector import connect

try:
    cnx = connect(host="localhost", database="test1", user="root", password="kalash72", port='3306')
    print("Connection successful")
    cnx.close()
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
