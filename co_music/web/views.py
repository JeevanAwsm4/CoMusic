import json
from random import randint

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect,JsonResponse,HttpResponse
from django.conf import settings
from django.db import IntegrityError

from web.models import Room,Music


@login_required(login_url='/users/login')
def index(request):
    context = {}

    return render(request,'web/index.html',context=context)

@login_required(login_url='/users/login')
def join_room(request,id):
    if Room.objects.filter(code=id,is_deleted=False).exists():
        room = Room.objects.get(code=id)
        files = Music.objects.filter(room=room)
        if room.is_user_in_room(request.user):
            context = {
                "room" : room,
                "files" : files,
                'media_root' : settings.MEDIA_URL,
            }
        else:
            room.add_user(request.user)
            context = {
                "room" : room,
                "files" : files,
                'media_root' : settings.MEDIA_URL,
            }
        return render(request,'web/playing.html',context=context)
    else:
        return JsonResponse({"error": True, "message": "Room does not exist!"})
    

@login_required(login_url='/users/login')
def create_room(request):
    while True:
        code = randint(100000, 999999)
        try:
            room = Room.objects.create(code=code, admin=request.user)
            room.add_user(request.user)
            break 
        except IntegrityError:
            continue
    
    return redirect('web:join_room', id=room.code)

@login_required(login_url='/users/login')
def delete_room(request,code):
    if Room.objects.filter(is_deleted=False,admin=request.user,code=code).exists():
        room = Room.objects.get(is_deleted=False,code=code)
        room.is_deleted = True
        room.save()

        response_data = {
            "status code" : 200,
            "message" : "Deleted successfully"
        }
        return HttpResponse(json.dumps(response_data))
    else:
        response_data = {
            "status code" : 404,
            "message" : "Room does not exist!"
        }
        return HttpResponse(json.dumps(response_data))
    
@login_required(login_url='/users/login')
def leave_room(request,code):
    if Room.objects.filter(is_deleted=False,code=code).exists():
        room = Room.objects.get(is_deleted=False,code=code)
        if request.user != room.admin:
            room.users.remove(request.user)
            room.save()

            response_data = {
                "status code" : 200,
                "message" : "You Left successfully"
            }   
            return HttpResponse(json.dumps(response_data))
        else:
            response_data = {
                "status code" : 403,
                "message" : "You are the admin.You are forbidden to leave"
            }   
            return HttpResponse(json.dumps(response_data))           
    else:
        response_data = {
            "status code" : 404,
            "message" : "Room does not exist!"
        }
        return HttpResponse(json.dumps(response_data))