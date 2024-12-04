
from django.contrib import admin
from django.urls import path
from referal_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('set/', views.set_session, name='set_session'),
    path('get/', views.get_session, name='get_session'),
    path('login/', views.login, name= 'login'),
]
