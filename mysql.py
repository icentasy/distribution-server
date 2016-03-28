import MySQLdb

class MySQL(object):
    def __init__(self, host, port, user, passwd, db="bank",):
        self.__conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)
        self.__conn.autocommit(False)
        self.__cur = self.__conn.cursor()

    def login(self, account, pw):
        self.__cur.execute("select count(*) from user where id=%s and pw=%s" % (account, pw))
        if self.__cur.fetchone()[0] == 1:
            return True
        else:
            return False

    def withdraw(self, account, cash, timestamp):
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)"
            % (account, 2, cash, timestamp)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            con.rollback()
            return False, None
        total = self.__cur.fetchone()[0]
        if (total - cash) < 0:
            con.rollback()
            return False, None
        if self.__cur.execute("update total set total=%s where id=%f" % (account, total - cash)) <= 0:
            con.rollback()
            return False, None
        con.commit()
        return True, total - cash
        

    def deposite(self, account, cash, timestamp):
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)"
            % (account, 3, cash, timestamp)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            con.rollback()
            return False, None
        total = self.__cur.fetchone()[0]
        if self.__cur.execute("update total set total=%s where id=%f" % (account, total + cash)) <= 0:
            con.rollback()
            return False, None
        con.commit()
        return True, total + cash


    def transfer(self, account, cash, timestamp, acID, acName):
        if self.__cur.execute("select count(*) from user where id=%s and name=%s" % (acID, acName)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)"
            % (account, 4, cash, timestamp)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            con.rollback()
            return False, None
        total = self.__cur.fetchone()[0]
        if (total - cash) < 0:
            con.rollback()
            return False, None
        if self.__cur.execute("update total set total=%s where id=%f" % (account, total - cash)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)"
            % (acID, 5, cash, timestamp)) <= 0:
            con.rollback()
            return False, None
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            con.rollback()
            return False, None
        acTotal = self.__cur.fetchone()[0]
        if self.__cur.execute("update total set total=%s where id=%f" % (account, acTotal + cash)) <= 0:
            con.rollback()
            return False, None
        con.commit()
        return True, total - cash

    def checkTotal(self, account):
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            return False, 0
        return True, self.__cur.fetchone()[0]
        
    def checkDetail(self, account):
        if self.__cur.execute("select * from detail where id=%s" % account) <= 0:
            return False, None
        return True, self.__cur.fetchall()