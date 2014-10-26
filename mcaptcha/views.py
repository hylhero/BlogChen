#-*- coding:utf-8 -*-
from django.http.response import HttpResponse, Http404
from mcaptcha import code
from cStringIO import StringIO
import random
import json


def mcaptcha(request, key):
    co = code.Captcha()
    co_strs = co.captcha()
    out = StringIO()
    co.img.save(out, "PNG")
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    response['string'] = co_strs

    return response


def mcaptcha_refresh(request):
    if not request.is_ajax():
        raise Http404
    print request.is_ajax(), '::', request.POST
    return HttpResponse(json.dumps({'img': random.randint(100)}), content_type='application/json')
