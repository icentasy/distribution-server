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
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)" \
            % (account, 2, cash, timestamp)) <= 0:
            self.__conn.rollback()
            return False, "insert value failed!"
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            self.__conn.rollback()
            return False, "there is not total record!"
        total = self.__cur.fetchone()[0]
        if (total - cash) < 0:
            self.__conn.rollback()
            return False, "there is not enough money to withdraw"
        if self.__cur.execute("update total set total=%f where id=%s" % (total - cash, account)) <= 0:
            self.__conn.rollback()
            return False, "total can't be update!"
        self.__conn.commit()
        return True, total - cash
        

    def deposite(self, account, cash, timestamp):
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)" \
            % (account, 3, cash, timestamp)) <= 0:
            self.__conn.rollback()
            return False, "insert value failed!"
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            self.__conn.rollback()
            return False, "there is not total record!"
        total = self.__cur.fetchone()[0]
        if self.__cur.execute("update total set total=%f where id=%s" % (total + cash, account)) <= 0:
            self.__conn.rollback()
            return False, "total can't be update!"
        self.__conn.commit()
        return True, total + cash


    def transfer(self, account, cash, timestamp, acID, acName):
        if self.__cur.execute("select count(*) from bank.user where id=%s and name='%s'" % (acID, acName)) <= 0:
            self.__conn.rollback()
            return False, "the name and id is not match about the accept ID"
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)" \
            % (account, 4, cash, timestamp)) <= 0:
            self.__conn.rollback()
            return False, "insert transfer out value failed!"
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            self.__conn.rollback()
            return False, "there is not transfer-out ID's total record!"
        total = self.__cur.fetchone()[0]
        if (total - cash) < 0:
            self.__conn.rollback()
            return False, "there is not enough money to transfer"
        if self.__cur.execute("update total set total=%f where id=%s" % (total - cash, account)) <= 0:
            self.__conn.rollback()
            return False, "transfer out total can't be update"
        if self.__cur.execute("insert into detail (id, type, cash, timestamp) values(%s, %d, %f, %s)" \
            % (acID, 5, cash, timestamp)) <= 0:
            self.__conn.rollback()
            return False, "insert transfer in value failed!"
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            self.__conn.rollback()
            return False, "there is not transfer-in ID's total record!"
        acTotal = self.__cur.fetchone()[0]
        if self.__cur.execute("update total set total=%f where id=%s" % (acTotal + cash, account)) <= 0:
            self.__conn.rollback()
            return False, "transfer in total can't be update"
        self.__conn.commit()
        return True, total - cash

    def checkTotal(self, account):
        if self.__cur.execute("select total from total where id=%s" % account) <= 0:
            return False, 0
        return True, self.__cur.fetchone()[0]
        
    def checkDetail(self, account):
        if self.__cur.execute("select * from detail where id=%s" % account) <= 0:
            return False, None
        return True, self.__cur.fetchall()