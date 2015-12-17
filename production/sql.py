import pymysql.cursors
import config


class SQL():

	def __init__(self,username='',password=''):
		self.connection = pymysql.connect(host=config.host,
			user=config.user,
			password=config.password,
			db=config.db,
			charset='utf8mb4',
			cursorclass=pymysql.cursors.DictCursor)

	def inputTicker(ty,subty,side,trend,inst,price,change,seqID,volume):
		time = 
		sql = 'INSERT INTO `sttcrawler`.`ticker` (`time`, `type`, `subtype`, `side`, `trend`, `instrument`, `price`, `change`, `seqID`, `volume`) VALUES (\''+time+'\', '1', '2', '3', '4', '5', '6', '7', '8', '9', );"
																																								ty,subty,side,trend,inst,price,change,seqID,volume
# with connection.cursor() as cursor:
# # Create a new record
# sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
# cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

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


# with connection.cursor() as cursor:
# # Create a new record
# sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
# cursor.execute(sql, ('webmaster@python.org', 'very-secret'))


