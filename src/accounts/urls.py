from django.urls import path
from accounts import views
from django.contrib.auth import logout

urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_login_email'),
    path('login', views.login, name='login'),
    path('logout', logout, {'next_page': '/'}, name='logout'),
]