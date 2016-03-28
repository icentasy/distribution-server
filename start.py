# -*- coding: utf-8 -*-
import sys
sys.path.append("./")
from queue import RedisQueue
from mysql import MySQL

requestQ = RedisQueue("request", host="115.159.69.54")
con = MySQL(host="115.159.69.54", db="bank", user="root", passwd="gyhy")
print con.login('1','1')