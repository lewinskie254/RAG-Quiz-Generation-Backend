# my_app/urls.py
from django.urls import path
from .views import StudentView, SchoolView, CourseView, TeacherView, QuizView, UnitView

app_name = 'api' 
urlpatterns = [
    path('student/<str:action>/', StudentView.as_view(), name='add-student'), 
    path('student/<str:action>/<str:id>/', StudentView.as_view(), name='student-details'), 
    path('school/<str:action>/', SchoolView.as_view(), name='add-school'), 
    path('school/<str:action>/<str:id>/', SchoolView.as_view(), name='school-details'), 
    path('teacher/<str:action>/', TeacherView.as_view(), name='add-teacher'), 
    path('teacher/<str:action>/<str:id>/', TeacherView.as_view(), name='teacher-details'), 
    path('course/<str:action>/', CourseView.as_view(), name='add-course'), 
    path('course/<str:action>/<str:id>/', CourseView.as_view(), name='course-details'), 
    path('unit/<str:action>/', UnitView.as_view(), name='add-unit'), 
    path('unit/<str:action>/<str:id>/', UnitView.as_view(), name='unit-details'), 
    path('quiz/<str:action>/', QuizView.as_view(), name='add-quiz'), 
    path('quiz/<str:action>/<str:id>/', QuizView.as_view(), name='quiz-details'), 
    path('quiz/<str:action>/<str:id>/<str:instance>/', QuizView.as_view(), name='generate-and-set-quiz'), 
]