__author__ = 'vincent'
import redis
import datavbizdbtest
import time

def dictredis(dicname,value,time):
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    r.delete(dicname)
    r.hmset(dicname,value)
    r.expire(dicname,time)
    return(r.hgetall(dicname))

def listredis(listname,listvalue,time):

    r.delete(listname)
    r.lpush(listname,listvalue)
    r.expire(listname,time)
    return(r.lrange(listname,0,-1))

def rentalamount(ns):

    value=datavbizdbtest.rentalamount(ns)
    #print(value)
    name="rentalamount"+ns
    while True:
        dictredis(name,value,86400)
        data=r.hgetall("rentalamount{}".format(ns))
        time.sleep(82800)
    return data

def montharea(ns):

    value=datavbizdbtest.montharea(ns)
    #print(value)
    name="montharea"+ns
    while True:
        listredis(name,value,86400)
        data=r.lrange("montharea{}".format(ns),0,-1)[0]
        time.sleep(82800)
    return data

def occupancyrate(ns):

    value=datavbizdbtest.occupancyrate(ns)
    print(value)
    name="occupancyrate"+ns
    while True:
        listredis(name,value,86400)
        data=r.lrange("occupancyrate{}".format(ns),0,-1)[0]
        time.sleep(82800)
    return data


if __name__ == "__main__":
    dic={"a":1,"b":2}
    ns="999992"
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    #a= occupancyrate(ns)
    print(r.lrange("occupancyrate{}".format(ns),0,-1)[0])
    '''#a=rentalamount(ns)
    #print(a)
    a=r.hgetall("rentalamount{}".format(ns))
    if a=={}:
       rentalamount(ns)
       a=r.hgetall("rentalamount{}".format(ns))
    print(a)
    a=r.hgetall("a")
    key=dic["a"]
    while True:
        a=r.hgetall("a")

        dic["a"]=key+1
        dictredis("a",dic,10)
        a=r.hgetall("a")
        key=dic["a"]
        print(a)
        time.sleep(9)'''


