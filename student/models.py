import uuid
from django.db import models

# Create your models here.
class School(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='school-id')
    name = models.CharField(max_length=200, null=False, help_text='school-name')
    email = models.CharField(max_length=200, null=False, unique=True, help_text='school-email')
    phone_number = models.CharField(max_length=20, null=False, unique=True, help_text='school-phone-number')
    location = models.CharField(max_length=200, null=False,help_text='school-location')

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='teacher-id')
    name = models.CharField(max_length=200, null=False, help_text='teacher-name')
    phone_number = models.CharField(max_length=20, null=False, unique=True, help_text='teacher-phone-number')
    school = models.ForeignKey(School, on_delete=models.CASCADE,null=False, default=uuid.uuid4)


class Course(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='course-id')
    name = models.CharField(max_length=200, null=False, help_text='course-name')
    teacher =  models.ForeignKey(Teacher, on_delete=models.CASCADE,null=False)
    units = models.IntegerField(default=0)




class Student(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='student-id')
    name = models.CharField(max_length=200, null=False, help_text='student-name')
    email = models.CharField(max_length=200, null=True, unique=True, help_text='student-email')
    phone_number = models.CharField(max_length=20, null=True,unique=True, help_text='student-phone-number')
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