from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Teacher, Student, User, School, Course

class SchoolSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = School
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Course
        fields = "__all__"

class UnitSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Unit
        fields = "__all__"

class QuizSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Quiz
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Question
        fields = "__all__"

class ChoiceSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Choice
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Teacher
        fields = "__all__"
   


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"



class StudentUnitScoreSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StudentUnitScore
        fields = "__all__"