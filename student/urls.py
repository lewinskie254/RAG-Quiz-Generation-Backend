# my_app/urls.py
from django.urls import path
from .views import StudentView, SchoolView

app_name = 'student' # Define an app namespace for unique URL names

urlpatterns = [
    path('student/<str:action>/', StudentView.as_view(), name='add-student'), 
    path('student/<str:action>/<str:instance>/', StudentView.as_view(), name='student-details'), 
    path('school/<str:action>/', SchoolView.as_view(), name='add-school'), 
    path('school/<str:action>/<str:instance>/', SchoolView.as_view(), name='school-details'), 
]