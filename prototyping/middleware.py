# encoding: utf-8

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse, HttpResponseServerError
from django.template import Context, Template

class LoginLinkMiddleware(object):
    def __init__(self):
        pass
        
    def process_response(self, request, response):
        login = request.GET.get('login', 'false')
        if login=='true':
            response.content = response.content.replace('.html"', '.html?login=true"')
        else:
            response.content = response.content.replace('.html"', '.html?login=false"')
        return response

