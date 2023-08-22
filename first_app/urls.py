from django.urls import path, include
from first_app import views

app_name = 'first_app'

urlpatterns = [
    path('other/', views.other, name='other'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login')
]