from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class StudentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Student
        fields = "__all__"

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

class Choices(serializers.ModelSerializer): 
    class Meta: 
        model = Choices
        fields = "__all__"