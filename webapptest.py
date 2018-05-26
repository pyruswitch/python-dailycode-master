# -*- coding: utf-8 -*-
__author__ = 'vincent'
from flask import Flask
from flask import request
import json
import ehbizdatatest
from flask import Flask, Response
from flask_cors import *
from flask import Response
import time
import datetime
from werkzeug.datastructures import Headers



class MyResponse(Response):
    def __init__(self, response=None, **kwargs):
        headers = {"Access-Control-Allow-Origin": "*",
               "Access-Control-Allow-Credentials": 'true',
               "Access-Control-Allow-Headers": "Referer,User-Agent,Origin, X-Requested-With, Content-Type, Accept, X-ID, X-TOKEN, X-ANY-YOUR-CUSTOM-HEADER",
               "Access-Control-Allow-Methods": "POST, PUT, GET, OPTIONS, DELETE"}
        kwargs['headers'] = headers
        return super().__init__(response, **kwargs)

def create_app():
    app = Flask(__name__)
    starttime=""
    endtime=""
    #app.response_class = MyResponse
    CORS(app , supports_credentials=True)
    @app.route('/', methods=['GET', 'POST'])
    def home():

         return "Hello, cross-origin-world!"
    @app.route('/searchtime', methods=['GET', 'POST'])
    def stime():
        #data=request.form.get('data','')
        nonlocal starttime,endtime
        starttime=request.form.get('starttime','')
        endtime=request.form.get('endtime', '')
        print("选择的startime:"+str(starttime))
        print("选择的endtime:"+str(endtime))
        if starttime=="":
            starttime= datetime.date.today() - datetime.timedelta(days=60)
            endtime= datetime.date.today() + datetime.timedelta(days=1)
        dict={"starttime":str(starttime),"endtime":str(endtime)}
        dict=json.dumps(dict,ensure_ascii=False)
        return dict
    @app.route('/income', methods=['GET', 'POST'])
    def income():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print("现在执行income")
        print(now)
        #timedict=stime()
        #print(timedict)

        #try:
           #starttime= eval(timedict)["starttime"]
           #endtime=eval(timedict)["endtime"]
        print("更新startime:"+str(starttime))
        print("更新endtime:"+str(endtime))
        #except Exception:
            #print("没有执行try")
            #starttime= datetime.date.today() - datetime.timedelta(days=60)
            #endtime= datetime.date.today() + datetime.timedelta(days=1)
        print(now)
        list1,list2,list3,list4,list5,list6=ehbizdatatest.incomedata(starttime,endtime)
        dict={"daylist":list1,"onlineincome":list2,"lineincome":list3,"shop":list4,"shopincome":list5,"intotal":list6}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/powerincome', methods=['GET', 'POST'])
    def powerincome():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list4,list5=ehbizdatatest.powerincomedata(starttime,endtime)
        dict={"daylist":list1,"shop":list4,"shopincome":list5}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/lunch', methods=['GET', 'POST'])
    def lunch():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.lunchdata(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict

    @app.route('/lunchsupplier', methods=['GET', 'POST'])
    def lunchsupplier():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.suppliersaledata(starttime,endtime)
        dict={"daylist":list1,"suplist":list2,"supnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict

    @app.route('/wastage', methods=['GET', 'POST'])
    def wastage():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.shopwastagedata(starttime,endtime)
        dict={"daylist":list1,"waslist":list2,"supwaslist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/catsale', methods=['GET', 'POST'])
    def catesale():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.catesaledata(starttime,endtime)
        dict={"daylist":list1,"catenamelist":list2,"catnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/teccatsale', methods=['GET', 'POST'])
    def teccatesale():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.teccatesaledata(starttime,endtime)
        dict={"daylist":list1,"catenamelist":list2,"catnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/user', methods=['GET', 'POST'])
    def user():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3,list4=ehbizdatatest.userdata(starttime,endtime)
        dict={"daylist":list1,"totaluserlist":list2,"onlineuserlist":list3,"lineuserlist":list4}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/onlineshopuser', methods=['GET', 'POST'])
    def onlineshopuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.onlineshopuserdata(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/lineshopuser', methods=['GET', 'POST'])
    def lineshopuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.lineshopuserdata(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/newuser', methods=['GET', 'POST'])
    def newuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3,list4=ehbizdatatest.newusertype(starttime,endtime)
        dict={"daylist":list1,"totaluserlist":list2,"onlineuserlist":list3,"lineuserlist":list4}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/onnewshopuser', methods=['GET', 'POST'])
    def onnewshopuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.onlinenewuser(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/linenewshopuser', methods=['GET', 'POST'])
    def linenewshopuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.linenewuser(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/benefitalldata', methods=['GET', 'POST'])
    def benefitalldata():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3,list4=ehbizdatatest.benefitalldata(starttime,endtime)
        dict={"daylist":list1,"discountlist":list2,"activilist":list3,"totallist":list4}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/shopdiscount', methods=['GET', 'POST'])
    def shopdiscount():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.shopdiscount(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/shopactivity', methods=['GET', 'POST'])
    def shopactivity():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdatatest.shopactivity(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/lossuser', methods=['GET', 'POST'])
    def lossuser():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1=ehbizdatatest.lossuser()
        dict={"lossuser":list1}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    return app

if __name__ == '__main__':
    app=create_app()
    app.debug = True
    app.run(port =8080,threaded=True)