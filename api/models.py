import uuid
from django.db import models

# Create your models here.
class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200)


class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, unique=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="teachers"
    )


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    total_units = models.IntegerField(default=0)


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="students"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="students"
    )
    grade = models.IntegerField(default=0)




class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="units"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="units"
    )
    total_score = models.IntegerField(default=100)  # still recommended to remove

class StudentUnitScore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


class Quiz(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )
    number_of_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Question(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=2000)


class Choices(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    content = models.CharField(max_length=500)
