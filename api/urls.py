# my_app/urls.py
from django.urls import path
from .views import StudentView, SchoolView, CourseView, TeacherView

app_name = 'api' # Define an app namespace for unique URL names

urlpatterns = [
    path('student/<str:action>/', StudentView.as_view(), name='add-student'), 
    path('student/<str:action>/<str:instance>/', StudentView.as_view(), name='student-details'), 
    path('school/<str:action>/', SchoolView.as_view(), name='add-school'), 
    path('school/<str:action>/<str:instance>/', SchoolView.as_view(), name='school-details'), 
    path('teacher/<str:action>/', TeacherView.as_view(), name='add-teacher'), 
    path('teacher/<str:action>/<str:instance>/', TeacherView.as_view(), name='teacher-details'), 
    path('course/<str:action>/', CourseView.as_view(), name='add-course'), 
    path('course/<str:action>/<str:instance>/', CourseView.as_view(), name='course-details'), 
]