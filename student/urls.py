# my_app/urls.py
from django.urls import path
from .views import StudentView

app_name = 'student' # Define an app namespace for unique URL names

urlpatterns = [
    path('<str:action>/', StudentView.as_view(), name='register-student'), 
    path('<str:action>/<str:instance>/', StudentView.as_view(), name='get-or-update-student')
]