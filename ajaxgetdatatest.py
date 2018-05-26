__author__ = 'vincent'
# -*- coding: utf-8 -*-

def application(environ, start_response):
     start_response('200 OK', [('Content-Type', 'text/html')])
     body = '1234'
     return [body.encode('utf-8')]