import uuid
from django.db import models

# Create your models here.
class School(models.Model):
    school_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='school-id')
    school_name = models.CharField(max_length=200, null=False, help_text='school-name')


class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='course-id')
    course_name = models.CharField(max_length=200, null=False, help_text='course-name')

class Student(models.Model): 
    student_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='student-id')
    student_name = models.CharField(max_length=200, null=False, help_text='student-name')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    grade = models.IntegerField(default=0) 

class Unit(models.Model):
    unit_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='unit-id')
    unit_course = models.ForeignKey(Course,on_delete=models.CASCADE,null=False)
    unit_score= models.IntegerField(default=0) 

class Quiz(models.Model): 
    quiz_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='quiz-id') 
    quiz_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE,null=False)
    number_of_questions = models.IntegerField(default=0) 

class Question(models.Model): 
    question_id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid.uuid4, help_text='question-id')
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE,null=False)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=2000)
