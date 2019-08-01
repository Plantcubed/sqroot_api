# log/views.py
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from ipware.ip import get_ip
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.template.response import TemplateResponse
from .forms import PasswordResetRequestForm
from .forms import PasswordChangeRequestForm
from .forms import NewUserForm
from django.template import Context, loader
from django.db import models
import json

# views are all managed from here
def checkForAuth(request, redirect):
    if request.user.is_authenticated():
        return render(request, redirect, { 'remote' : 'remote'})
    else:
        ip = get_ip(request)
        if ip is not None:
            # if '127.0.0.1' or '192.168.0.209' in ip:
            if '127.0.0.1' in ip:
                return render(request, redirect, { 'local' : 'local'})
            else:
                return HttpResponseRedirect('login/')
        else:
            return HttpResponseRedirect('login/')


def home(request):
    return checkForAuth(request, 'index.html')


def recipe(request):
    return checkForAuth(request, 'recipe.html')


def images(request):
    return checkForAuth(request, 'images.html')


def control(request):
    return checkForAuth(request, 'control.html')


def about(request):
    return checkForAuth(request, 'about.html')


def setup(request):
    return checkForAuth(request, 'setup.html')


def useradd(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            current_site = get_current_site(request)

            context = {
                'form': NewUserForm,
                'site': current_site,
                'site_name': current_site.name,
                'reset': 'no',
            }
            return TemplateResponse(request, 'users/add.html', context)
        elif request.method == 'POST':
            try:
                passWord = request.POST.get("password", "")
                eMail = request.POST.get("email", "")
                userName = request.POST.get("username", "")
                confirmpassWord = request.POST.get("confirmpassword", "2kds9u3ehjdfea")
                if confirmpassWord != passWord:
                    return TemplateResponse(request, 'users/fail.html',{'failmessage': 'Passwords do not match', 'reset': 'no', })
                if not passWord or not eMail or not userName:
                    return TemplateResponse(request, 'users/fail.html', {'failmessage': 'Fields cannot be blank', 'reset': 'no',})
            except:
                return TemplateResponse(request, 'users/fail.html', {'failmessage': 'Unknown error', 'reset': 'no',})

            user = User.objects.create_user(userName, eMail, passWord)
            user.is_active = True
            user.save()
            return HttpResponseRedirect('/')


def userresetpassword(request):
    if request.method == 'GET':
        current_site = get_current_site(request)

        context = {
            'form': PasswordResetRequestForm,
            'site': current_site,
            'site_name': current_site.name,
            'reset' : 'reset',
        }
        return TemplateResponse(request, 'users/reset.html', context)
    elif request.method == 'POST':
        try:
            userName = request.POST.get("username", "")
        except:
            return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Username missing', 'reset': 'no',})

        if userName:
            count = User.objects.count()
            for x in range(1, count + 1):
                try:
                    aobj = User.objects.get(id=x)
                    if aobj.get_username() == userName:
                        password = User.objects.make_random_password(length=8)
                        passwordmsg = 'Your new password is ' + password
                        res = aobj.email_user('Your New Password',
                                              passwordmsg,
                                              'sqroot@plantcubed.com')
                        aobj.set_password(password)
                        aobj.save()
                        return HttpResponseRedirect('login/')
                except User.DoesNotExist:
                    break
            return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Username not found', 'reset': 'no',})
        else:
            return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Username cannot be blank', 'reset': 'no',})

@csrf_exempt
def userlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            # Load the template myblog/templates/index.html
            template = loader.get_template('users/list.html')

            # Context is a normal Python dictionary whose keys can be accessed in the template index.html
            count = User.objects.count()
            userlist = []
            for x in range(1, count + 1):
                userlist.append(User.objects.get(id=x).username)

            current_site = get_current_site(request)
            context = Context({
                'site': current_site,
                'site_name': current_site.name,
                'user_list': userlist,
                'reset': 'no',
            })
            return TemplateResponse(request, 'users/list.html', context)
        elif request.method == 'POST':
            userName = request.POST.get("user", "")
            count = User.objects.count()
            for x in range(1, count + 1):
                aobj = User.objects.get(id=x)
                if aobj.get_username() == userName:
                    if x == 0:
                        return TemplateResponse(request, 'users/fail.html', {'failmessage': 'Cannot delete primary user'})
                    User.objects.get(id=x).delete()
                    return HttpResponseRedirect('/')
            return TemplateResponse(request, 'users/fail.html', {'failmessage': 'User not found'})


def userchangepassword(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            current_site = get_current_site(request)

            context = {
                'form': PasswordChangeRequestForm,
                'site': current_site,
                'site_name': current_site.name,
                'reset' : 'reset',
            }
            return TemplateResponse(request, 'users/change.html', context)
        elif request.method == 'POST':
            try:
                passWord = request.POST.get("password", "")
                confirmpassWord = request.POST.get("confirmpassword", "2kds9u3ehjdfea")
                userName = request.POST.get("username", "")
                if passWord != confirmpassWord:
                    return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Passwords do not match'})
            except:
                return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Unknown error'})

            if userName:
                count = User.objects.count()
                for x in range(1, count + 1):
                    try:
                        aobj = User.objects.get(id=x)
                        if aobj.get_username() == userName:
                            password = passWord
                            passwordmsg = 'Your password password had been chagned'
                            res = aobj.email_user('Your Password',
                                                  passwordmsg,
                                                  'sqroot@plantcubed.com')
                            aobj.set_password(password)
                            aobj.save()
                            return HttpResponseRedirect('/')
                    except User.DoesNotExist:
                        break
                return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Username Invalid'})
            else:
                return TemplateResponse(request, 'users/fail.html', { 'failmessage': 'Username Invalid'})

