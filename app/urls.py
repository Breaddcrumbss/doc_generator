from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('generate', views.generate, name='generate'),
    path('manage', views.manage, name='manage'),
    path('delete/<id>', views.delete_template, name='delete-template')


]
