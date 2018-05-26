
# -*- coding: utf-8 -*-
__author__ = 'vincent'
from wsgiref.simple_server import make_server

from asyncloadhtml import application

port = 54407
httpd = make_server('', port, application)
print("你可以访问  http://localhost:" + str(port) + "/")

httpd.serve_forever()
