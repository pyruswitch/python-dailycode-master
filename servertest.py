__author__ = 'vincent'
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
import bizdata
#from ajaxgetdatatest import application


def application(environ, start_response):
     start_response('200 OK',
                    [ ('Content-Type', 'text/html'),
                      ('Access-Control-Allow-Origin', '*'),
     	              ('Access-Control-Allow-Methods', 'GET, POST'),
     	              ('Access-Control-Allow-Headers', 'X-Requested-With, content-type')
                      ])
     method = environ['REQUEST_METHOD']
     path = environ['PATH_INFO']

     if method=='GET' and path=='/a':
       dayinlist ,onlineincom_list,lineincom_list,shoplist,shopnumlist,dayintal_list=bizdata.incomedata()
       body =bizdata.datahtmlstr(onlineincom_list)
       return [body.encode('utf-8')]
     body = str([1,2,3,4])
     return [body.encode('utf-8')]
port = 54309
httpd = make_server('localhost', port, application)
print("你可以访问  http://localhost:" + str(port) + "/")

httpd.serve_forever()
