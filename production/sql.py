import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='sttcrawler',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `ticker`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()