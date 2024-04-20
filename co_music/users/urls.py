from django.urls import path,include

from users.views import login,signup


app_name = "users"

urlpatterns = [
    path('login/',login,name='login'),
    path('signup/',signup,name='signup'),
]
