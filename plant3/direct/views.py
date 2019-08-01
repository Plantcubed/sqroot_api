from direct.models import Direct
from direct.models import Runs
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from django.shortcuts import redirect
import uuid
import json
import time


@csrf_exempt
@never_cache
def index(request):
    if request.method == 'GET':
        try:
            dobj = Direct.objects.get(id=1)
        except Direct.DoesNotExist:
            newobj = Direct.objects.create(
                command="",
                command_timestamp=int(time.time()),
                command_waitto=0,
                command_timeo = False,
                command_rdy=False,
                results="",
                results_timestamp=int(time.time()),
                results_rdy=False)
            dobj = Direct.objects.get(id=1)

            # if busy check the command to
        if dobj.command_rdy == True:
            if (dobj.command_waitto + dobj.command_timestamp) < int(time.time()):
                dobj.command_rdy = False
                dobj.command_timeo = True
                dobj.save()
                # serialize data
        s = serializers.serialize('json', [Direct.objects.get(id=1)])
        js = json.loads(s)
        out = str(js[0]['fields'])
        out = out.replace("'", '"')
        # needed to clean out th False
        out = out.replace('False', 'false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        return HttpResponse(status=503)

@csrf_exempt
@never_cache
def execute(request):
    if request.method == 'GET':
        return HttpResponse(status=503)
    elif request.method == 'POST':
        # post new command
        dobj = Direct.objects.get(id=1)
        # see if a command is running
        if dobj.command_rdy == True:
            # command is running, has it to'ed
            if (dobj.command_waitto + time.time()) < int(time.time()):
                dobj.command_rdy = False
                dobj.command_timeo = True
                dobj.save()
            else:
                return HttpResponse(status=503)
        # OK, ready to write command data
        # get json command
        data = json.loads(request.body.decode('utf-8'))
        # stuff it into api
        dobj.command_rdy = True
        dobj.command_timestamp = int(time.time())
        dobj.command_waitto = data['command_waitto']
        dobj.command_timeo = False
        dobj.command = data['command']
        dobj.results_rdy = False
        dobj.results_timestamp = 0
        dobj.results = ""
        dobj.save()
        return HttpResponse(status=200)


@csrf_exempt
@never_cache
def response(request):
    if request.method == 'GET':
        return HttpResponse(status=400)
    elif request.method == 'POST':
        # post new command
        dobj = Direct.objects.get(id=1)
        # see if a command is running
        if dobj.command_rdy == False:
            # no?, why are we responding
            return HttpResponse(status=401)
        # OK, ready to write command data
        # get json command
        data = json.loads(request.body.decode('utf-8'))
        # stuff it into api
        dobj.command_rdy = False
        dobj.results = data['response']
        dobj.results_rdy = True
        dobj.results_timestamp = int(time.time())
        dobj.save()
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def current_run(request):
    if request.method == 'GET':
        try:
            s = serializers.serialize('json', [Runs.objects.get(id=1)])
        except:
            return HttpResponse(status=500)
        js = json.loads(s)
        out = str(js[0]['fields'])
        out = out.replace("'", '"')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        try:
            dobj = Runs.objects.get(id=1)
        except:
            return HttpResponse(status=500)
        data = json.loads(request.body.decode('utf-8'))
        dobj.current_run = data['current_run']
        dobj.save()
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def current_run_index(request):
    if request.method == 'GET':
        try:
            s = serializers.serialize('json', [Runs.objects.get(id=1)])
        except:
            return HttpResponse(status=500)
        js = json.loads(s)
        out = str(js[0]['fields'])
        out = out.replace("'", '"')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        try:
            dobj = Runs.objects.get(id=1)
        except:
            return HttpResponse(status=500)
        data = json.loads(request.body.decode('utf-8'))
        dobj.current_run_index = data['current_run_index']
        dobj.save()
        return HttpResponse(status=200)

def tojsonaddurlindex(request, s, index):
    js = json.loads(s)
    z = str(js[0]['fields'])
    z = z.replace("'", '"')
    return '{"url": "' + request.build_absolute_uri() + str(index) + '/",' + z[1:]

def tojsonaddurl(request, s):
    js = json.loads(s)
    z = str(js[0]['fields'])
    z = z.replace("'", '"')
    return '{"url": "' + request.build_absolute_uri() + '",' + z[1:]
