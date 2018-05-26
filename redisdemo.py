__author__ = 'vincent'
import redis
import datavbizdb
from threading import Timer
import datetime
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler


def dictredis(dicname,value,time):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    r.delete(dicname)
    r.hmset(dicname,value)
    if time !="":
       r.expire(dicname,time)
    return(r.hgetall(dicname))

def listredis(listname,listvalue,time):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    r.delete(listname)
    r.lpush(listname,listvalue)
    r.expire(listname,time)
    return(r.lrange(listname,0,-1))

def setredis(name,value,time):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    r.delete(name)
    r.lpush(name,value)
    r.expire(name,time)
    return(r.get(name))

def rentalamount(ns):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    name="rentalamount"+ns

    value=datavbizdb.rentalamount(ns)
    dictredis(name,value,86400)

    data=r.hgetall("rentalamount{}".format(ns))
    #time.sleep(82800)
    return data

def montharea(ns):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    #print(value)
    name="montharea"+ns
    value=datavbizdb.montharea(ns)
    value=str(value)
    listredis(name,value,86400)
    data=r.lrange("montharea{}".format(ns),0,-1)[0]
    #time.sleep(82800)
    return data

def occupancyrate(ns):

    value=datavbizdb.occupancyrate(ns)
    print(value)
    name="occupancyrate"+ns
    while True:
        listredis(name,value,86400)
        data=r.lrange("occupancyrate{}".format(ns),0,-1)[0]
        #time.sleep(82800)
    return data


if __name__ == "__main__":
    dic={"a":1,"b":2} 
    ns="23"
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    #a= occupancyrate(ns)
    #print(r.lrange("occupancyrate{}".format(ns),0,-1))
    #montharea(ns)
    a=r.lrange("montharea{}".format(ns),0,-1)
    print(r.lrange("montharea{}".format(ns),0,-1))
    if a==[]:
        montharea(ns)
        print(r.lrange("montharea{}".format(ns),0,-1)[0])
    #print(r.hgetall("rentalamount{}".format(ns)))


