import MySQLdb

class MySQL(object):
	def __init__(self, host, port, user, passwd, db="bank",):
		self.__conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
		self.__cur = self.__conn.cursor()

	def login(self, account, pw):
		self.__cur.excute("select count(*) from user where id=%s and pw=%s" % (account, pw))
		if self.__cur.fetchOne() == 1:
			return True
		else:
			return False