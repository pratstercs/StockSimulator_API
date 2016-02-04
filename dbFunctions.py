from cassandra.cluster import Cluster
import cassandra.util

dbConnection = None

def testDbConnection():
	global dbConnection
	if dbConnection == null:
		dbConnection = initSession()

#connect to the Cassandra database
def initSession():
	cluster = Cluster(['91.121.25.208'])
	session = cluster.connect('nyse')
	return session

def getSymbol(session, symbol):
	rows = session.execute('SELECT * FROM ' + symbol)
	return rows

def printRows(resultSet):
	for row in resultSet:
		print row[0], row[1], row[2], row[3], row[4]

def arrayToDatabase(session,array):
	for row in array:
		print(row)
		rowToDatabase(session, row)

def rowToDatabase(session, array):
	date = dateTimeToMillis(array[0])
	op = array[1]
	hi = array[2]
	lo = array[3]
	cl = array[4]
	vol = int(array[5])
	uid = genUUID(array[0])

	session.execute(
		"""
		INSERT INTO jpm (uid, date, open, high, low, close, volume)
		VALUES(%s, %s, %s, %s, %s, %s, %s)
		""",
		(uid, date, op, hi, lo, cl, vol)
	)