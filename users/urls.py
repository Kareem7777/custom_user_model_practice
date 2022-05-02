from django.urls import path
from users.views import *
urlpatterns = [
  path('home', home, name='home_url'),
  path('register', register_view, name='register_url'),
  path('login/', login_view, name='login_url'),
  path('logout', logout_view, name='logout_url'),
]
