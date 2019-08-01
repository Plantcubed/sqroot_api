from django.shortcuts import render
from revisions.models import Revision
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import HttpResponse
import json

@csrf_exempt
@never_cache
def revision(request):
    if request.method == 'GET':
        count = 1
        out = ""
        while True:
            try:
                aobj = Revision.objects.get(id=count)
                s = serializers.serialize('json', [Revision.objects.get(id=count)])
                out += tojsonaddurlindex(request, s, count)  + ','
                count += 1
            except Revision.DoesNotExist:
                if count > 0:
                    count -= 1
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")

    elif request.method == 'POST':
        # find next item
        count = 1
        while True:
            try:
                aobj = Revision.objects.get(id=count)
                count += 1
            except Revision.DoesNotExist:
                break
        # decode data
        data = json.loads(request.body.decode('utf-8'))
        # load the data
        newobj = Revision.objects.create(
            name=data['name'],
            major=data['major'],
            minor=data['minor'],
            build=data['build'])
        return HttpResponse(count, content_type="application/json")

@csrf_exempt
@never_cache
def revisionitem(request, revision_id):
    if request.method == 'GET':
        s = serializers.serialize('json', [Revision.objects.get(id=revision_id)])
        out = tojsonaddurl(request,s)
        # needed to clean out th False
        out = out.replace('False','false')
        out = out.replace('True', 'true')
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # decode data
        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)
        try:
            aobj = Revision.objects.get(id=revision_id)
            aobj.name = data['name']
            aobj.major = data['major']
            aobj.minor = data['minor']
            aobj.build = data['build']
            aobj.save()
        except Revision.DoesNotExist:
            return HttpResponse(status=204)
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

