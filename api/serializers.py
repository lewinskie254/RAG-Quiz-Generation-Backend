from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

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

class ChoicesSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Choices
        fields = "__all__"

from rest_framework import serializers
from .models import Teacher, Student, User, School, Course

class TeacherSerializer(serializers.ModelSerializer):
    # Accept username & password to create User
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Teacher
        fields = ["id", "username", "password", "name", "phone_number", "school"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        
        # Create User with hashed password
        user = User.objects.create_user(username=username, password=password, role="teacher")
        
        # Create Teacher profile
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Student
        fields = ["id", "username", "password", "name", "email", "phone_number", "course", "school", "grade"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        
        # Create User with hashed password
        user = User.objects.create_user(username=username, password=password, role="student")
        
        # Create Student profile
        student = Student.objects.create(user=user, **validated_data)
        return student


class StudentUnitScoreSerializer(serializers.ModelSerializer):
    class Meta: 
        model = StudentUnitScore
        fields = "__all__"