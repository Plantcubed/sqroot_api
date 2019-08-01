from actuators.models import Actuator
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import time

@csrf_exempt
@never_cache
def index(request):
    if request.method == 'GET':
        count = Actuator.objects.count()
        out = ""
        for x in range(1, count+1):
            try:
                aobj = Actuator.objects.get(id=x)
                s = serializers.serialize('json', [Actuator.objects.get(id=x)])

                # adjust override
                if aobj.override == True:
                    # check the time
                    if aobj.override_end < int(time.time()):
                        aobj.override = False
                        #aobj.value = aobj.pre_over_value
                        aobj.save()

                out += tojsonaddurlindex(request, s, x)  + ','
            except Actuator.DoesNotExist:
                break
        out = out[:-1]
        # needed to clean out th False
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")
    # adds a new actuator
    elif request.method == 'POST':
        # find next item
        count = Actuator.objects.count()
        # decode data
        data = json.loads(request.body.decode('utf-8'))
        # load the data
        newobj = Actuator.objects.create(
            name = data['name'],
            index = count+1,
            instruction_code = data['instruction_code'],
            instruction_id = data['instruction_id'],
            extra = data['extra'],
            value = data['value'],
            pre_over_value = data['value'],
            timestamp = time.time(),
            override = False,
            override_start = time.time(),
            override_end = time.time(),
            value_min=data['value_min'],
            value_max = data['value_max'],
            error_state = data['error_state'],
            dose_to = data['dose_to'])
        return HttpResponse(count, content_type="application/json")

@csrf_exempt
@never_cache
def item(request,actuators_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Actuator.objects.get(id=actuators_id)])
        out = tojsonaddurl(request,s)
        # needed to clean out th False
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    # modifys an existing acutator
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        try:
            aobj = Actuator.objects.get(id=actuators_id)
            aobj.name = data['name']
            aobj.index = actuators_id
            aobj.instruction_code = data['instruction_code']
            aobj.instruction_id = data['instruction_id']
            aobj.extra = data['extra']
            aobj.value = data['value']
            aobj.pre_over_value = data['value']
            aobj.value_min = data['value_min']
            aobj.value_max = data['value_max']
            aobj.error_state = data['error_state']
            aobj.dose_to = data['dose_to']
            aobj.override = False
            aobj.override_start = time.time()
            aobj.override_end = time.time()
            aobj.save()
        except Actuator.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def error(request,actuators_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Actuator.objects.get(id=actuators_id)], fields=('error_state'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Actuator.objects.get(id=actuators_id)
            aobj.error = data['error_state']
            aobj.save()
        except Actuator.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def dose_to(request,actuators_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Actuator.objects.get(id=actuators_id)], fields=('dose_to'))
        out = tojsonaddurl(request, s)
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Actuator.objects.get(id=actuators_id)
            aobj.dose_to = data['dose_to']
            aobj.save()
        except Actuator.DoesNotExist:
            return HttpResponse(status=204)
        return HttpResponse(status=200)

@csrf_exempt
@never_cache
def value(request,actuators_id):
    if request.method == 'GET':
        # perform override check
        aobj = Actuator.objects.get(id=actuators_id)
        if aobj.override == True:
            # check the time
            if aobj.override_end < int(time.time()):
                aobj.override = False
                #aobj.value = aobj.pre_over_value
                aobj.save()
        s = serializers.serialize('json', [Actuator.objects.get(id=actuators_id)], fields=('value', 'timestamp', 'override', 'override_start', 'override_end'))
        out = tojsonaddurl(request, s)
        # needed to clean out th False
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        # get object
        try:
            aobj = Actuator.objects.get(id=actuators_id)
            aobj.pre_over_value = aobj.value
            aobj.value = data['value']
            aobj.timestamp = time.time()
            aobj.override = data['override']
            aobj.override_start = time.time()
            aobj.override_end = time.time() + data['override_duration']
            aobj.save()
            return HttpResponse(status=200)
        except Actuator.DoesNotExist:
            return HttpResponse(status=204)


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

