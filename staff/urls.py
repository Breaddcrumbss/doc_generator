from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('login_staff/', views.login_staff, name='login'),
    path('registration/', views.register_staff, name='registration'),
    path('logout_staff/', views.user_logout, name='logout')

]