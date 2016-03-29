# -*- coding: utf-8 -*-
import sys
sys.path.append("./")
import json

from queue import RedisQueue
from mysql import MySQL

requestQ = RedisQueue("request", host="115.159.69.54")
con = MySQL("115.159.69.54", 3306, user="root", passwd="gyhy")

while  True:
	req = requestQ.get()
	if req is None:
		continue
	print req
	res = {"status":0, "errorMsg":"", "data": None}
	resData = {"sum": 0}
	reqJson = json.loads(req)
	tradeType = reqJson.get("type")
	account = reqJson.get("id")
	pw = reqJson.get("pw")
	timestamp = reqJson.get("timestamp")
	data = reqJson.get("data")
	if tradeType == 0:
		res["status"] = con.login(account, pw)
	elif tradeType == 2:
		cash = data.get("cash")
		status, total = con.withdraw(account, cash, timestamp)
		res["status"] = status
		if status:
			resData["sum"] = total
		else:
			res["errorMsg"] = total
	elif tradeType == 3:
		cash = data.get("cash")
		status, total = con.deposite(account, cash, timestamp)
		res["status"] = status
		if status:
			resData["sum"] = total
		else:
			res["errorMsg"] = total
	elif tradeType == 4:
		cash = data.get("cash")
		acID = data.get("acID")
		acName = data.get("acName")
		status, total = con.transfer(account, cash, timestamp, acID, acName)
		res["status"] = status
		if status:
			resData["sum"] = total
		else:
			res["errorMsg"] = total
	elif tradeType == 6:
		status, total = con.checkTotal(account)
		res["status"] = status
		resData["sum"] = total
	elif tradeType == 7:
		status, detail = con.checkDetail(account)
		res["status"] = status
		resData = []
		for item in detail:
			resData.append({
				"type": item[1],
				"cash": item[2],
				"timestamp": item[3],
				"transferid": item[4]
				})
	res["data"] = resData
	requestQ.set("%s_%s" % (account, timestamp), json.dumps(res))


