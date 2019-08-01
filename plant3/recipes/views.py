from recipes.models import Recipe
from recipes.models import RecipeRuns
from recipes.models import RecipeControl
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import os, shutil, json, time

class InvalidTimeString(Exception):
    pass


@csrf_exempt
@never_cache
def index(request):
    if request.method == 'GET':
        index = 1
        count = 0
        out = ""
        while True:
            try:
                aobj = Recipe.objects.get(id=index)
                if aobj.type == 0:
                    s = serializers.serialize('json', [Recipe.objects.get(id=index)])
                    out += tojsonaddurlindex(request, s, count)  + ','
                    count += 1
                index += 1
            except Recipe.DoesNotExist:
                if index > 0:
                    index -= 1
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        # upload a recipe
        fname = request.POST.get('name')
        fdesc = request.POST.get('description')
        types = request.POST.get('type')
        s = request.FILES['file']
        Recipe.objects.create(
            name = fname,
            description = fdesc,
            index = Recipe.objects.count() + 1,
            type = types,
            file = s)
        return HttpResponse(status=200)


@csrf_exempt
@never_cache
def indexhidden(request):
    if request.method == 'GET':
        index = 1
        count = 0
        out = ""
        while True:
            try:
                aobj = Recipe.objects.get(id=index)
                s = serializers.serialize('json', [Recipe.objects.get(id=index)])
                out += tojsonaddurlindex(request, s, count)  + ','
                count += 1
                index += 1
            except Recipe.DoesNotExist:
                if index > 0:
                    index -= 1
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        return HttpResponse(status=226)


@csrf_exempt
@never_cache
def clear(request):
    if request.method == 'GET':
        return HttpResponse(status=226)
    elif request.method == 'POST':
        # clear recipe and recipe history database
        data = json.loads(request.body.decode('utf-8'))
        code = data['code']
        out = "code is " + code;
        if code == 'All':
            # delete recipes
            delete_recipes()
            # delete run data
            delete_runs()
            # delete history
            delete_history()
            return HttpResponse(status=200)
        elif code == 'Recipes':
            # delete recipes
            delete_recipes()
            return HttpResponse(status=200)
        elif code == 'Runs':
            # delete run data
            delete_runs()
            return HttpResponse(status=200)
        elif code == 'History':
            # delete run data
            delete_history()
            return HttpResponse(status=200)

        return HttpResponse(status=204)


@csrf_exempt
@never_cache
def runstop(request):
    if request.method == 'GET':
        return HttpResponse(status=204)
    elif request.method == 'POST':
        #find the last recipe
        count = RecipeRuns.objects.count()

        try:
            aobj = RecipeRuns.objects.get(id=count)
        except:
            return HttpResponse(status=200)

        # only modify if the recipe is currently running
        if aobj.end_timestamp > time.time():
            aobj.end_timestamp = time.time()
        aobj.save()

        # kill current recipe
        robj = RecipeControl.objects.get(id=1)
        robj.current_run = 0
        robj.current_recipe = 0
        robj.save()

        return HttpResponse(status=200)


@csrf_exempt
@never_cache
def get(request,recipes_id):
    if request.method == 'GET':
        aobj = RecipeRuns.objects.get(id=1)
        return HttpResponse(aobj.recipe, content_type="application/json")


@csrf_exempt
@never_cache
def runs(request):
    if request.method == 'GET':
        # returns a json formatted list of current recipes runs
        count = 1
        out = ""
        while True:
            try:
                s = serializers.serialize('json', [RecipeRuns.objects.get(id=count)])
                out += tojsonaddurlindex(request, s, count)  + ','
                count += 1
            except:
                if count > 0:
                    count -= 1
                break
        out = out[:-1]
        out = '{ "count":' + str(count) + ', "results": [' + out + ']}'
        return HttpResponse(out, content_type="application/json")
    elif request.method == 'POST':
        fail = 0
        # passed an index to the recipes and starts that run on the server
        # get json data
        data = json.loads(request.body.decode('utf-8'))
        #find the recipe
        # this adds 2 to skip by the startup and shutdown recipes
        recipe_idx = data['recipe']
        try:
            aobj = Recipe.objects.get(id=recipe_idx)
        except:
            # does not exist
            return HttpResponse(status=204)

        #find the last recipe
        count = RecipeRuns.objects.count();

        # get the last recipe
        if count != 0:
            lastrunsobj = RecipeRuns.objects.get(id=count)
            # if the end time is greater than curret, we are still running it
            if lastrunsobj.end_timestamp > int(time.time()):
                return HttpResponse(status=503)

        # create new run record
        # set times
        start_time = time.time()
        end_time = 0
        # parse file to find the end
        count = 1
        injson = ""
        read_data = ""
        #jsonfile = open('/var/www/plant3/media/' + aobj.file.name, 'rt')
        with open('/var/www/plant3/media/' + aobj.file.name, 'rt') as f:
            read_data += f.read()
        #return HttpResponse(read_data)
        filejson = json.loads(read_data)

        operationsjson = filejson['operations']

        linejson = operationsjson[0]
        start_time = linejson[0]
        #for a in range(0,len(operationsjson)):
        #    linejson = operationsjson[a]
        #    timejson = linejson[0]

        linejson = operationsjson[len(operationsjson)-1]
        end_time = linejson[0]

        if  end_time < start_time:
            return  HttpResponse(status=416)
        # create record of the run
        newobj = RecipeRuns.objects.create(
            recipe = aobj,
            start_timestamp = start_time + time.time(),
            end_timestamp = end_time + time.time(),
            name = aobj.name)

        # indicate a new recipe is loaded
        robj = RecipeControl.objects.get(id=1)
        # the current run in runs
        robj.current_run = RecipeRuns.objects.count()
        # the current recipe
        robj.current_recipe = recipe_idx
        robj.save()

        return HttpResponse(status=200)


@csrf_exempt
@never_cache
def control(request):
    if request.method == 'GET':
        try:
            s = serializers.serialize('json', [RecipeControl.objects.get(id=1)])
            js = json.loads(s)
            z = str(js[0]['fields'])
            z = z.replace("'", '"')
            out = z
            return HttpResponse(out, content_type="application/json")
        except:
            # does not exist
            return HttpResponse(status=204)
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        typee = data['type']
        # is type in range
        if typee < 0 or typee > 2:
            return HttpResponse(status=204)

        try:
            robj = Recipe.objects.get(id=data['recipe'])
        except:
            # does not exist
            return HttpResponse(status=204)

        try:
            aobj = RecipeControl.objects.get(id=1)

            if typee == 1:
                aobj.startup = robj
            elif typee == 2:
                aobj.shutdown = robj
            else:
                # shoud never get here
                return HttpResponse(status=500)
            aobj.save
            return HttpResponse(status=201)
        except RecipeControl.DoesNotExist:
            if typee == 1:
                newobj = RecipeControl.objects.create(startup=robj,shutdown=robj)
            elif typee == 2:
                newobj = RecipeControl.objects.create(startup=robj,shutdown=robj)
            return HttpResponse(status=202)


def delete_history():
    # remove all history in database
    # find number of records
    count = 1
    while True:
        try:
            RecipeRuns.objects.get(id=count)
            count += 1
        except:
            if count > 0:
                count -= 1
            break
    # remove all recipes in database
    count = RecipeRuns.objects.count();
    for x in range(1, count + 1):
        RecipeRuns.objects.get(id=x).delete()


def rm_rf(d):
    for path in (os.path.join(d, f) for f in os.listdir(d)):
        if os.path.isdir(path):
            rm_rf(path)
        else:
            os.unlink(path)
    os.rmdir(d)


def delete_runs():
    # delete files in runs directory
    try:
        rm_rf('/var/www/plant3/media/runs/')
        #shutil.rmtree('/var/www/plant3/media/runs/')
    except Exception as e:
        pass


def delete_recipes():
    # delete recipe files
    folder = '/var/www/plant3/media/recipes'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            pass

    # remove all recipes in database
    count = Recipe.objects.count();
    for x in range(1, count+1):
        Recipe.objects.get(id=x).delete()


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


def parse_time_string(time_string):
    time_args = time_string.split(b':')
    if len(time_args) != 4:
        raise InvalidTimeString()
    try:
        time_args = [int(arg) for arg in time_args]
    except ValueError:
        raise InvalidTimeString()
    return time_args.pop() + 60 * time_args.pop() + 60 * 60 * time_args.pop() + \
           60 * 60 * 24 * time_args.pop()