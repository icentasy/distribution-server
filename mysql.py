import MySQLdb

class MySQL(object):
	def __init__(self, db="bank", **kwargs):
		self.__conn = MySQLdb.connect(kwargs)
		self.__cur = __conn.cursor()

	def login(account, pw):
		self.__cur.excute("select count(*) from user where id=%s and pw=%s" % (account, pw))
		if self.__cur.fetchOne() == 1:
			return True
		else:
			return False