import uuid
from django.db import models

# Create your models here.
class School(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='school-id')
    name = models.CharField(max_length=200, null=False, help_text='school-name')


class Course(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='course-id')
    name = models.CharField(max_length=200, null=False, help_text='course-name')

class Student(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='student-id')
    name = models.CharField(max_length=200, null=False, help_text='student-name')
    email = models.CharField(max_length=200, null=True, help_text='student-email')
    phone_number = models.CharField(max_length=20, null=True, help_text='student-phone-number')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE,null=False,)
    grade = models.IntegerField(default=0) 

class Unit(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='unit-id')
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    score= models.IntegerField(default=0) 

class Quiz(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='quiz-id') 
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE,null=False)
    number_of_questions = models.IntegerField(default=0) 

class Question(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='question-id')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,null=False)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=2000)

class Choices(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='multiple-choice-id')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    content = models.CharField(max_length=500)