from django.contrib import admin
from django.urls import path,include

from web.views import index,join_room,create_room,delete_room,leave_room


app_name = 'web'

urlpatterns = [
    path('',index,name='index'),
    path('room/<int:id>',join_room,name='join_room'),
    path('create_room/',create_room,name='create_room'),
    path('delete_room/<int:code>',delete_room,name='delete_room'),
    path('leave_room/<int:code>',leave_room,name='leave_room'),
]
