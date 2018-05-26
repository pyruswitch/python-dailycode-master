__author__ = 'vincent'
from flask import request
import json
from flask_cors import CORS, cross_origin
from flask import Response
import datavbizdb
from flask import Flask
#from redisdemo import dataredis
import time
import redis
import redisdemo
import staticdata



def create_app():

    app = Flask(__name__)
    CORS(app , supports_credentials=True)

    ns=""

    @app.route('/', methods=['GET', 'POST'])
    def home():

         return "Hello, cross-origin-world!"
    @app.route('/evh/datav/parkorder', methods=['GET', 'POST'])
    def parkorder():

        ns =request.values.get("ns")
        try:
          if ns in ("999969","999955"):

             allorderdata=staticdata.parkorder(ns)
             allorderdata=allorderdata
          else:
             allorderdata=datavbizdb.parkorder(ns)
          dict={"errorCode": "200","errorDescription": "OK","response":allorderdata}

          dict=json.dumps(dict,ensure_ascii=False)
          return dict
        except Exception:
           dict={"errorCode": "200","errorDescription": "OK","response":{}}
           dict=json.dumps(dict,ensure_ascii=False)
           return dict
    @app.route('/evh/datav/ordertypecount', methods=['GET', 'POST'])
    def ordertypecount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):

               ordertypecount=staticdata.ordertypecount(ns)
               ordertypecount=ordertypecount
            else:
               ordertypecount=datavbizdb.ordertypecount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":ordertypecount}
            #ordertypecount:订单类型个数
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/ordertypeamount', methods=['GET', 'POST'])
    def ordertypeamount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):

               ordertypeamount=staticdata.ordertypeamount(ns)
               ordertypeamount=ordertypeamount
            else:
               ordertypeamount=datavbizdb.ordertypeamount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":ordertypeamount}
            #ordertypecount:订单类型总额
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/orderchannelcount', methods=['GET', 'POST'])
    def orderchannelcount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):

               orderchannelcount=staticdata.orderchannelcount(ns)
               orderchannelcount=orderchannelcount
            else:
              orderchannelcount=datavbizdb.orderchannelcount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":orderchannelcount}
            #orderchannelcount:订单渠道总额
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/monthamount', methods=['GET', 'POST'])
    def monthamount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               monthamount=staticdata.monthamount(ns)
               monthamount=monthamount
            else:
               monthamount=datavbizdb.monthamount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":monthamount}
            #monthamount:订单每月总额
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/monthcount', methods=['GET', 'POST'])
    def monthcount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               monthcount=staticdata.monthcount(ns)
               monthcount=monthcount
            else:
              monthcount=datavbizdb.monthcount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":monthcount}
            #monthmonthcount:订单每月数量
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/orderamount', methods=['GET', 'POST'])
    def orderamount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               orderamount=staticdata.orderamount(ns)
               orderamount=orderamount
            else:
              orderamount=datavbizdb.orderamount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":orderamount}
            #orderamount:订单每月数量
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/ordercount', methods=['GET', 'POST'])
    def ordercount():
        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               ordercount=staticdata.ordercount(ns)
               ordercount=ordercount
            else:
             ordercount=datavbizdb.ordercount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":ordercount}
            #ordercount:订单每月数量
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/tasktypecount', methods=['GET', 'POST'])
    def tasktypecount():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               tasktypecount=staticdata.tasktypecount(ns)
               tasktypecount=tasktypecount
            else:
              tasktypecount=datavbizdb.tasktypecount(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":tasktypecount}
            #ordercount:任务类型分布
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/boardvita', methods=['GET', 'POST'])
    def boardvita():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               boardvita=staticdata.boardvita(ns)
               boardvita=boardvita
            else:
              boardvita=datavbizdb.boardvita(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":boardvita}
            #ordercount:模块活跃度
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/taskclose', methods=['GET', 'POST'])
    def taskclose():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               taskclose=staticdata.taskclose(ns)
               taskclose=taskclose
            else:
              taskclose=datavbizdb.taskclose(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":taskclose}
            #ordercount:已完成任务
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/daytaskorder', methods=['GET', 'POST'])
    def daytaskorder():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               daytaskorder=staticdata.daytaskorder(ns)
               daytaskorder=daytaskorder
            else:
              daytaskorder=datavbizdb.daytaskorder(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":daytaskorder}
            #ordercount:每日任务数
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/tasktyperespon', methods=['GET', 'POST'])
    def tasktyperespon():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               tasktyperespon=staticdata.tasktyperespon(ns)
               tasktyperespon=tasktyperespon
            else:
               tasktyperespon=datavbizdb.tasktyperespon(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":tasktyperespon}
            #ordercount:平均响应时间
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/pengdingtask', methods=['GET', 'POST'])
    def  pengdingtask():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               pengdingtask=staticdata.pengdingtask(ns)
               pengdingtask=pengdingtask
            else:
              pengdingtask=datavbizdb. pengdingtask(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": pengdingtask}
            #ordercount:代办任务
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/taskstatus', methods=['GET', 'POST'])
    def  taskstatus():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               taskstatus=staticdata.taskstatus(ns)
               taskstatus=taskstatus
            else:
              taskstatus=datavbizdb. taskstatus(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": taskstatus}
            #ordercount:任务状态分布
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/totalassets', methods=['GET', 'POST'])
    def  totalassets():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               totalassets=staticdata.totalassets(ns)
               totalassets=totalassets
            else:
               totalassets=datavbizdb. totalassets(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": totalassets}
            #ordercount:总产值
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/Companyespon', methods=['GET', 'POST'])
    def  Companyespon():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               Companyespon=staticdata.Companyespon(ns)
               Companyespon=Companyespon
            else:
               Companyespon=datavbizdb. Companyespon(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": Companyespon}
            #企业名册
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/settledenter', methods=['GET', 'POST'])
    def  settledenter():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               settledenter=staticdata.settledenter(ns)
               settledenter=settledenter
            else:
               settledenter=datavbizdb. settledenter(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": settledenter}
            #入驻企业情况
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict

    @app.route('/evh/datav/InviteBusiness', methods=['GET', 'POST'])
    def   InviteBusiness():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               InviteBusiness=staticdata.InviteBusiness(ns)
               InviteBusiness=InviteBusiness
            else:
              InviteBusiness=datavbizdb.  InviteBusiness(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":  InviteBusiness}
            #入驻企业情况
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/Companytype', methods=['GET', 'POST'])
    def   Companytype():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               Companytype=staticdata.Companytype(ns)
               Companytype=Companytype
            else:
               Companytype=datavbizdb.Companytype(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":  Companytype}
            #入驻企业情况
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/occupancyrate', methods=['GET', 'POST'])
    def occupancyrate():

        ns =request.values.get("ns")

        try:
            if ns in ("999969","999955"):
               occupancyrate=staticdata.occupancyrate(ns)
               occupancyrate=occupancyrate
            else:
              occupancyrate=datavbizdb.occupancyrate(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":  occupancyrate}
            #入驻企业情况
            dict=json.dumps(dict,ensure_ascii=False)

            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/rentalamount', methods=['GET', 'POST'])
    def rentalamount():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               rentalamount=staticdata.rentalamount(ns)
               rentalamount=rentalamount
            else:
                rentalamount=r.hgetall("rentalamount{}".format(ns))

                if rentalamount=={}:
                    redisdemo.rentalamount(ns)
                    rentalamount=r.hgetall("rentalamount{}".format(ns))
            #rentalamount=list(rentalamount)
            dict={"errorCode": "200","errorDescription": "OK","response":  rentalamount}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict

    @app.route('/evh/datav/unitrental', methods=['GET', 'POST'])
    def unitrental():

        ns =request.values.get("ns")
        try:
            #unitrental=datavbizdb.rentalamount(ns)
            unitrental={"name":"单位租金","value":0}
            dict={"errorCode": "200","errorDescription": "OK","response":  unitrental}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/leasedarea', methods=['GET', 'POST'])
    def leasedarea():

        ns =request.values.get("ns")
        try:
            leasedarea=datavbizdb.leasedarea(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": leasedarea}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/montharea', methods=['GET', 'POST'])
    def montharea():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               montharea=staticdata.montharea(ns)
               montharea=montharea
            else:
               montharea=datavbizdb.montharea(ns)

            dict={"errorCode": "200","errorDescription": "OK","response": montharea}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/totalenergy', methods=['GET', 'POST'])
    def mtotalenergy():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               totalenergy=staticdata.totalenergy(ns)
               totalenergy=totalenergy
            else:
              totalenergy=datavbizdb.totalenergy(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": totalenergy}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/buildmonthwatermeter', methods=['GET', 'POST'])
    def buildmonthwatermeter():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               buildmonthwatermeter=staticdata.buildmonthwatermeter(ns)
               buildmonthwatermeter=buildmonthwatermeter
            else:
              buildmonthwatermeter=datavbizdb.buildmonthwatermeter(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": buildmonthwatermeter}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/buildmonthelectr', methods=['GET', 'POST'])
    def buildmonthelectr():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               buildmonthelectr=staticdata.buildmonthelectr(ns)
               buildmonthelectr=buildmonthelectr
            else:
               buildmonthelectr=datavbizdb.buildmonthelectr(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": buildmonthelectr}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/watermetercureading', methods=['GET', 'POST'])
    def watermetercureading():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               watermetercureading=staticdata.watermetercureading(ns)
               watermetercureading=watermetercureading
            else:
               watermetercureading=datavbizdb.watermetercureading(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": watermetercureading}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/electrmetercureading', methods=['GET', 'POST'])
    def electrmetercureading():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               electrmetercureading=staticdata.electrmetercureading(ns)
               electrmetercureading=electrmetercureading
            else:
               electrmetercureading=datavbizdb.electrmetercureading(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": electrmetercureading}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict

    @app.route('/evh/datav/qualityinspetask', methods=['GET', 'POST'])
    def qualityinspetask():

        ns =request.values.get("ns")
        try:
            qualityinspetask=datavbizdb.qualityinspetask(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": qualityinspetask}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/equipmentinspetask', methods=['GET', 'POST'])
    def equipmentinspetask():

        ns =request.values.get("ns")
        try:
            equipmentinspetask=datavbizdb.equipmentinspetask(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": equipmentinspetask}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/todayquality', methods=['GET', 'POST'])

    def todayquality():

        ns =request.values.get("ns")
        try:
            todayquality=datavbizdb.todayquality(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": todayquality}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict

    @app.route('/evh/datav/todayequipment', methods=['GET', 'POST'])

    def todayequipment():

        ns =request.values.get("ns")
        try:
            todayequipment=datavbizdb.todayequipment(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": todayequipment}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/inspectiontasktype', methods=['GET', 'POST'])

    def inspectiontasktype():
        ns =request.values.get("ns")
        try:
            inspectiontasktype=datavbizdb.inspectiontasktype(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": inspectiontasktype}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/activityenrollment', methods=['GET', 'POST'])
    def activityenrollment():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               activityenrollment=staticdata.activityenrollment(ns)
               activityenrollment=activityenrollment
            else:
               activityenrollment=datavbizdb.activityenrollment(ns)
            dict={"errorCode": "200","errorDescription": "OK","response": activityenrollment}
            #年租金
            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"Exception": Exception}
           return dict
    @app.route('/evh/datav/forumthreads', methods=['GET', 'POST'])
    def forumthreads():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               forumthreads=staticdata.forumthreads(ns)
               forumthreads=forumthreads
            else:
              forumthreads=datavbizdb.forumthreads(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":forumthreads}

            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/activitytype', methods=['GET', 'POST'])
    def activitytype():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               activitytype=staticdata.activitytype(ns)
               activitytype=activitytype
            else:
               activitytype=datavbizdb.activitytype(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":activitytype}

            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/activityattention', methods=['GET', 'POST'])
    def activityattention():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               activityattention=staticdata.activityattention(ns)
               activityattention=activityattention
            else:
               activityattention=datavbizdb.activityattention(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":activityattention}

            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/trendingtopics', methods=['GET', 'POST'])
    def trendingtopics():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               trendingtopics=staticdata.trendingtopics(ns)
               trendingtopics=trendingtopics
            else:
              trendingtopics=datavbizdb.trendingtopics(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":trendingtopics}

            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/newactivity', methods=['GET', 'POST'])
    def newactivity():

        ns =request.values.get("ns")
        try:
            if ns in ("999969","999955"):
               newactivity=staticdata.newactivity(ns)
               newactivity=newactivity
            else:
               newactivity=datavbizdb.newactivity(ns)
            dict={"errorCode": "200","errorDescription": "OK","response":newactivity}

            dict=json.dumps(dict,ensure_ascii=False)
            return dict
        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/newforum', methods=['GET', 'POST'])
    def newforum():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   newforum=staticdata.newforum(ns)
                   newforum=newforum
                else:
                   newforum=datavbizdb.newforum(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":newforum}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/communityuseract', methods=['GET', 'POST'])
    def communityuseract():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   communityuseract=staticdata.communityuseract(ns)
                   communityuseract=communityuseract
                else:
                   communityuseract=datavbizdb.communityuseract(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":communityuseract}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/daynewusertrend', methods=['GET', 'POST'])
    def daynewusertrend():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   daynewusertrend=staticdata.daynewusertrend(ns)
                   daynewusertrend=daynewusertrend
                else:
                   daynewusertrend=datavbizdb.daynewusertrend(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":daynewusertrend}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/dayactusertrend', methods=['GET', 'POST'])
    def dayactusertrend():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   dayactusertrend=staticdata.dayactusertrend(ns)
                   dayactusertrend=dayactusertrend
                else:
                   dayactusertrend=datavbizdb.dayactusertrend(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":dayactusertrend}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/daytotalusertrend', methods=['GET', 'POST'])
    def daytotalusertrend():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   daytotalusertrend=staticdata.daytotalusertrend(ns)
                   daytotalusertrend=daytotalusertrend
                else:
                  daytotalusertrend=datavbizdb.daytotalusertrend(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":daytotalusertrend}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/usergender', methods=['GET', 'POST'])
    def usergender():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   usergender=staticdata.usergender(ns)
                   usergender=usergender
                else:
                   usergender=datavbizdb.usergender(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":usergender}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    @app.route('/evh/datav/ostype', methods=['GET', 'POST'])
    def ostype():

        ns =request.values.get("ns")
        try:
                if ns in ("999969","999955"):
                   ostype=staticdata.ostype(ns)
                   ostype=ostype
                else:
                   ostype=datavbizdb.ostype(ns)
                dict={"errorCode": "200","errorDescription": "OK","response":ostype}

                dict=json.dumps(dict,ensure_ascii=False)
                return dict

        except Exception:
           dict={"response": "Exception"}
           return dict
    return app


if __name__ == '__main__':
    r=redis.Redis(host='127.0.0.1',port=6379,decode_responses=True)
    app=create_app()
    app.debug = True
    app.run(host='0.0.0.0',port=3001,threaded=True)