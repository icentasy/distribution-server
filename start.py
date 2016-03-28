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
	print "get sources"
	reqJson = json.loads(req)
	if reqJson.get("type") == 0:
		print con.login(reqJson.get("id"), reqJson.get("pw"))
		res = {"status":0}
		requestQ.set("%s_%s" % (reqJson.get("id"), reqJson.get("timestamp")), json.dumps(res))
