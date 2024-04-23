from django.contrib import admin
from django.urls import path,include

from web.views import index,join_room,create_room,delete_room,leave_room,upload_music,toggle_playback,update_position,get_song_data,fetch_next_song,get_playback_status


app_name = 'web'

urlpatterns = [
    path('',index,name='index'),
    path('room/<int:id>',join_room,name='join_room'),
    path('create_room/',create_room,name='create_room'),
    path('delete_room/<int:code>',delete_room,name='delete_room'),
    path('leave_room/<int:code>',leave_room,name='leave_room'),
    path('upload/<int:room_code>',upload_music,name='upload_music'),
    path('toggle_playback/<int:room_code>',toggle_playback,name='toggle_playback'),
    path('update_position/<int:room_code>/', update_position, name='update_position'),
    path('get_song_data/<int:room_code>/', get_song_data, name='get_song_data'),
    path('fetch_next_song/<int:room_code>/', fetch_next_song, name='fetch_next_song'),
    path('get_playback_status/<int:room_code>/', get_playback_status, name='get_playback_status'),
]
