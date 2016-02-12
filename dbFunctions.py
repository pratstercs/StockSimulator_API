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

def createTable(symbol):
	query = """
		CREATE TABLE IF NOT EXISTS nyse.{0} (
		    uid timeuuid,
		    date timestamp,
		    close decimal,
		    high decimal,
		    low decimal,
		    open decimal,
		    volume int,
		    PRIMARY KEY (uid, date)
		) WITH CLUSTERING ORDER BY (date DESC);
		""".format(symbol)
	dbConnection.execute(query)

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

def rowToDatabase(array, symbol):
	date = dateTimeToMillis(array[0])
	op = array[1]
	hi = array[2]
	lo = array[3]
	cl = array[4]
	vol = int(array[5])
	uid = genUUID(array[0])

	dbConnection.execute(
		"""
		INSERT INTO %s (uid, date, open, high, low, close, volume)
		VALUES(%s, %s, %s, %s, %s, %s, %s)
		""",
		(symbol, uid, date, op, hi, lo, cl, vol)
	)