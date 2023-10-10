from django.urls import path
from . import views

app_name = 'list_apps'

urlpatterns = [
	path('', views.index, name='index'),
]