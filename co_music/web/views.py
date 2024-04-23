import json
from random import randint

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect,JsonResponse,HttpResponse
from django.conf import settings
from django.db import IntegrityError

from web.models import Room,Music
from web.forms import MusicUploadForm


@login_required(login_url='/users/login')
def index(request):
    context = {}

    return render(request,'web/index.html',context=context)

@login_required(login_url='/users/login')
def join_room(request,id):
    if Room.objects.filter(code=id,is_deleted=False).exists():
        room = Room.objects.get(code=id)
        files = Music.objects.filter(room=room)
        form = MusicUploadForm()
        if room.is_user_in_room(request.user):
            context = {
                "room" : room,
                "files" : files.last(),
                'media_root' : settings.MEDIA_URL,
                'form' : form,
            }
        else:
            room.add_user(request.user)
            context = {
                "room" : room,
                "files" : files.first(),
                'media_root' : settings.MEDIA_URL,
                'form' : form,
            }
        return render(request,'web/music.html',context=context)
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


@login_required(login_url='/users/login')
def upload_music(request, room_code):
    room = get_object_or_404(Room, code=room_code, admin=request.user, is_deleted=False)
    
    if request.method == 'POST':
        form = MusicUploadForm(request.POST, request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.room = room
            music.is_queued = True
            music.save()

            response_data = {
                "status_code": 200,
                "message": "Music uploaded successfully."
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                "status_code": 400,
                "message": "Invalid form data."
            }
            return JsonResponse(response_data, status=400)
    else:
        response_data = {
            "status_code": 405,
            "message": "Method Not Allowed"
        }
        return JsonResponse(response_data, status=405)


def update_position(request, room_code):
    if request.method == 'POST':
        position = request.POST.get('position')
        music = Music.objects.filter(room__code=room_code).first()
        if music:
            music.current_position = position
            music.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Music object not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
def get_song_data(request, room_code):
    if request.method == 'GET':
        music = Music.objects.filter(room__code=room_code).first()
        if music:
            song_data = {
                'is_playing': music.is_playing,
                'current_position': music.current_position,
                'file_url': music.file.url if music.file else ''
            }
            return JsonResponse(song_data)
        else:
            return JsonResponse({'error': 'Music object not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def toggle_playback(request, room_code):
    if request.method == 'POST':
        music = Music.objects.filter(room__code=room_code).first()
        
        if music:
            music.is_playing = not music.is_playing
            if music.is_playing:
                position = request.POST.get('position')
                total = request.POST.get('length')
                music.current_position = position
                music.total_length = total
                
            music.save()
            
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Music object not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def fetch_next_song(request, room_code):
    if request.method == 'GET':
        room = Room.objects.get(code=room_code)
        next_song = Music.objects.filter(room=room, is_queued=True).first()
        if next_song:
            next_song.is_playing = True
            next_song.save()
            return JsonResponse({'next_song_url': next_song.file.url})
        else:
            return JsonResponse({'next_song_url': None})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def get_playback_status(request,room_code):
    if request.method == 'GET':
        music = Music.objects.filter(room__code=room_code).first()
        if music:
            response_data = {
                "status code" : 200,
                "is_playing" : music.is_playing,
                "current_position" : music.current_position,
                "total_length" : music.total_length,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Music object not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)