from django.shortcuts import render
from sensors.models import Sensor
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

@csrf_exempt
@never_cache
def index(request):
    if request.method == 'GET':
        count = Sensor.objects.count()
        out = ""
        for x in range(1, count + 1):
            try:
                aobj = Sensor.objects.get(id=x)
                s = serializers.serialize('json', [Sensor.objects.get(id=x)])
                out += tojsonaddurlindex(request, s, x)  + ','
            except Sensor.DoesNotExist:
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # find next item
        count = 1
        while True:
            try:
                aobj = Sensor.objects.get(id=count)
                count += 1
            except Sensor.DoesNotExist:
                break
        # decode data
        data = json.loads(request.body.decode('utf-8'))
        # load the data
        newobj = Sensor.objects.create(
            name = data['name'],
            index = count,
            instruction_code = data['instruction_code'],
            instruction_id = data['instruction_id'],
            extra = data['extra'],
            value = data['value'] )
        return HttpResponse(count, content_type="application/json")

@csrf_exempt
@never_cache
def item(request,sensor_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Sensor.objects.get(id=sensor_id)])
        out = tojsonaddurl(request,s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        try:
            # note that the index is not changed
            aobj = Sensor.objects.get(id=sensor_id)
            aobj.name = data['name']
            aobj.index = sensor_id
            aobj.instruction_code = data['instruction_code']
            aobj.instruction_id = data['instruction_id']
            aobj.extra = data['extra']
            aobj.value = data['value']
            aobj.save()
        except Sensor.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def value(request,sensor_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Sensor.objects.get(id=sensor_id)], fields=('value'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Sensor.objects.get(id=sensor_id)
            aobj.value = data['value']
            aobj.save()
        except Sensor.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def setpoint(request,sensor_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Sensor.objects.get(id=sensor_id)], fields=('setpoint'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Sensor.objects.get(id=sensor_id)
            aobj.setpoint = data['setpoint']
            aobj.save()
        except Sensor.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

def tojsonaddurlindex(request,s, index):
    js = json.loads(s)
    z = str(js[0]['fields'])
    z = z.replace("'", '"')
    return '{"url": "' + request.build_absolute_uri() + str(index) + '/",' + z[1:]

def tojsonaddurl(request,s):
    js = json.loads(s)
    z = str(js[0]['fields'])
    z = z.replace("'", '"')
    return '{"url": "' + request.build_absolute_uri() + '",' + z[1:]
