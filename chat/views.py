from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

import time
import datetime
import json
import uuid
from django_websocket import require_websocket

def index(request):
    print 'index'
    userid = uuid.uuid1()
    return render_to_response('chat/chat.html',{'userid':str(userid)},
                            context_instance=RequestContext(request))

def update(request):
    timeNow = datetime.datetime.now()
    print 'update'

    return HttpResponse('ok')

@require_websocket
def djWebSocket(request):
    print 'request.is_websocket()',request.is_websocket()
    message = request.websocket.wait()
    request.websocket.send(message)
    # for message in request.websocket:
    #     request.websocket.send(message)
    # return HttpResponse('ok')