# -*- coding: utf-8 -*-
__author__ = 'vincent'
from flask import Flask
from flask import request
import json
import ehbizdata
from flask import Flask
from flask_cors import CORS, cross_origin
from flask import Response
import time
import datetime



def create_app():
    app = Flask(__name__)
    CORS(app , supports_credentials=True)
    starttime=""
    endtime=""
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
        print(now)
        list1,list2,list3,list4,list5,list6=ehbizdata.incomedata("2017-10-18","2017-10-19")
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
        list1,list4,list5=ehbizdata.powerincomedata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.lunchdata(starttime,endtime)
        dict={"daylist":list1,"shoplist":list2,"shopnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict

    @app.route('/lunchsupplier', methods=['GET'])
    def lunchsupplier():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.suppliersaledata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.shopwastagedata(starttime,endtime)
        dict={"daylist":list1,"waslist":list2,"supwaslist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/breakfastft', methods=['GET', 'POST'])
    def breakfastft():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.ftbreakfastdata(starttime,endtime)
        dict={"daylist":list1,"prodnamelist":list2,"prodnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/breakfasttec', methods=['GET', 'POST'])
    def tecbreakfast():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.tecbreakfastdata(starttime,endtime)
        dict={"daylist":list1,"prodnamelist":list2,"prodnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/catsale', methods=['GET', 'POST'])
    def catesale():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.catesaledata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.teccatesaledata(starttime,endtime)
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
        list1,list2,list3,list4=ehbizdata.userdata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.onlineshopuserdata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.lineshopuserdata(starttime,endtime)
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
        list1,list2,list3,list4=ehbizdata.newusertype(starttime,endtime)
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
        list1,list2,list3=ehbizdata.onlinenewuser(starttime,endtime)
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
        list1,list2,list3=ehbizdata.linenewuser(starttime,endtime)
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
        list1,list2,list3,list4=ehbizdata.benefitalldata(starttime,endtime)
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
        list1,list2,list3=ehbizdata.shopdiscount(starttime,endtime)
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
        list1,list2,list3=ehbizdata.shopactivity(starttime,endtime)
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
        list1=ehbizdata.lossuser()
        dict={"lossuser":list1}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/ftaccountpro', methods=['GET', 'POST'])
    def ftaccountpro():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.ftaccountpro(starttime,endtime)
        dict={"daylist":list1,"catenamelist":list2,"catnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    @app.route('/tecaccountpro', methods=['GET', 'POST'])
    def tecaccountpro():
        ISOTIMEFORMAT='%Y-%m-%d %X'
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        list1,list2,list3=ehbizdata.tecaccountpro(starttime,endtime)
        dict={"daylist":list1,"catenamelist":list2,"catnumlist":list3}
        dict=json.dumps(dict,ensure_ascii=False)
        now =  time.strftime( ISOTIMEFORMAT, time.localtime() )
        print(now)
        return dict
    return app

if __name__ == '__main__':
    app=create_app()
    app.debug = True
    app.run(port=8080,threaded=True)