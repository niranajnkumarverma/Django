from django.urls import path
from .views import change_password, create_todo, delete_todo, otp_page, profile_update, profile_update_page, update_todo, index, logout, profile_page, register, register_page, signin, signin_page, verify_otp

urlpatterns = [
    path('', index),
    
    path('register_page/', register_page, name='register_page'),
    path('otp_page/', otp_page, name='otp_page'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('register/', register, name='register'),

    path('signin_page/', signin_page, name='signin_page'),
    path('signin/', signin, name='signin'),
    path('profile_page/', profile_page, name='profile_page'),
    path('profile_update_page/', profile_update_page, name='profile_update_page'),
    path('profile_update/', profile_update, name='profile_update'),
    path('change_password/', change_password, name='change_password'),
    
    path('create_todo/', create_todo, name='create_todo'),
    path('delete_todo/<int:pk>/', delete_todo, name='delete_todo'),
    path('update_todo/<int:pk>/', update_todo, name='update_todo'),
    
    path('logout/', logout, name='logout'),
]