from django.shortcuts import render
from controls.models import Control
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

@csrf_exempt
@never_cache
def index(request):
    if request.method == 'GET':
        count = 1
        out = ""
        while True:
            try:
                aobj = Control.objects.get(id=count)
                s = serializers.serialize('json', [Control.objects.get(id=count)])
                out += tojsonaddurlindex(request, s, count)  + ','
                count += 1
            except Control.DoesNotExist:
                if count > 0:
                    count -= 1
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # find next item
        count = 1
        while True:
            try:
                aobj = Control.objects.get(id=count)
                count += 1
            except Control.DoesNotExist:
                break
        # decode data
        data = json.loads(request.body.decode('utf-8'))
        # load the data
        newobj = Control.objects.create(
            name = data['name'],
            index = count,
            actuator_code = data['actuator_code'],
            actuator_id = data['actuator_id'],
            extra = data['extra'],
            sensor_id = data['sensor_id'],
            controller = data['controller'],
            sensor_code = data['sensor_code'],
            setpoint = data['setpoint'],
            command_code=data['command_code'],
            ctl_band_h = data['ctl_band_h'],
            ctl_band_l = data['ctl_band_l'],
            op_band_max = data['op_band_max'],
            op_band_min = data['op_band_min'],
            Kp = data['Kp'],
            Ki = data['Ki'],
            Kd = data['Kd'],
            dt = data['dt'],
            error = data['error'],
            enabled =data['enabled'] )
        return HttpResponse(count, content_type="application/json")

@csrf_exempt
@never_cache
def item(request,control_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Control.objects.get(id=control_id)])
        out = tojsonaddurl(request,s)
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        try:
            # note that the index is not changed
            aobj = Control.objects.get(id=control_id)
            aobj.name = data['name']
            aobj.index = control_id
            aobj.command_code = data['command_code']
            aobj.extra = data['extra']
            aobj.setpoint = data['setpoint']
            aobj.actuator_code = data['actuator_code']
            aobj.actuator_id = data['actuator_id']
            aobj.sensor_code = data['sensor_code']
            aobj.sensor_id = data['sensor_id']
            aobj.controller = data['controller']
            aobj.ctl_band_h = data['ctl_band_h']
            aobj.ctl_band_l = data['ctl_band_l']
            aobj.op_band_max = data['op_band_max']
            aobj.op_band_mim = data['op_band_min']
            aobj.Kp = data['Kp']
            aobj.Ki = data['Ki']
            aobj.Kd = data['Kd']
            aobj.dt = data['dt']
            aobj.error = data['error']
            aobj.enabled = data['enabled']
            aobj.save()
        except Control.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)


@csrf_exempt
@never_cache
def setpoint(request,control_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Control.objects.get(id=control_id)], fields=('setpoint'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Control.objects.get(id=control_id)
            aobj.setpoint = data['setpoint']
            aobj.save()
        except Control.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def enabled(request,control_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Control.objects.get(id=control_id)], fields=('enabled'))
        out = tojsonaddurl(request, s)
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Control.objects.get(id=control_id)
            aobj.enabled = data['enabled']
            aobj.save()
        except Control.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def error(request,control_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Control.objects.get(id=control_id)], fields=('error'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Control.objects.get(id=control_id)
            aobj.error = data['error']
            aobj.save()
        except Control.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def delete(request,control_id):
    if request.method == 'GET':
        return HttpResponse(status=204)
    elif request.method == 'POST':
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        try:
            Control.objects.get(id=control_id).delete()
            Control.objects.save()
        except Control.DoesNotExist:
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
