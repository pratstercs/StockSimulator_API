from cassandra.cluster import Cluster
import cassandra.util

dbConnection = None

def testDbConnection():
	global dbConnection
	if dbConnection == None:
		dbConnection = initSession()

#connect to the Cassandra database
def initSession():
	cluster = Cluster(['91.121.25.208'])
	session = cluster.connect('nyse')
	return session

def getSymbol(symbol):
	rows = dbConnection.execute('SELECT * FROM ' + symbol)
	return resultSetToArray(rows)

def resultSetToArray(resultSet):
	array = [list(row[1:]) for row in resultSet] #converts resultset (not including UUID) to array
	return array

def printRows(resultSet):
	for row in resultSet:
		print row[0], row[1], row[2], row[3], row[4]

def arrayToDatabase(array):
	for row in array:
		print(row)
		rowToDatabase(dbConnection, row)

def rowToDatabase(array):
	date = dateTimeToMillis(array[0])
	op = array[1]
	hi = array[2]
	lo = array[3]
	cl = array[4]
	vol = int(array[5])
	uid = genUUID(array[0])

	dbConnection.execute(
		"""
		INSERT INTO jpm (uid, date, open, high, low, close, volume)
		VALUES(%s, %s, %s, %s, %s, %s, %s)
		""",
		(uid, date, op, hi, lo, cl, vol)
	)