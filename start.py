# -*- coding: utf-8 -*-
import sys
sys.path.append("./")
from queue import RedisQueue

requestQ = RedisQueue("request", host="115.159.69.54")
print requestQ.size()
request.set("aaa")
print requestQ.size()