from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, Student, School
from ..serializers import *
from ..utils import serializer_checker, delete_element

class StudentView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-student": self.add_new_student,
            "update-student" : self.update_student, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    def get(self, request, action, id=None, instance=None):
        actions = {
            "show-student-details": self.show_student_details,
            "show-all-students-by-school" : self.show_all_students_by_school, 
            "show-all-students" : self.show_all_students, 
            "show-all-units-for-student" : self.show_all_units_for_student, 
            "delete-student" : self.delete_student, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    #add a new student 
    def add_new_student(self, request, id=None, instance=None): 
        course = get_object_or_404(Course, id=request.data.get("course"))
        school = get_object_or_404(School, id=request.data.get("school"))
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"message": "Missing username or password"}, status=400)

        # Create User first
        user = User.objects.create_user(
            username=username,
            password=password,
            role="student",
            email=request.data.get("email", "")
        )

        data = {
            "user": user.id,  # link User PK
            "name": request.data.get("name"),
            "phone_number": request.data.get("phoneNumber"),
            "course": course.id,  # pass PKs if serializer uses PrimaryKeyRelatedField
            "school": school.id,
            "grade": 0
        }

        # Check required fields
        required_fields = ["name", "phone_number"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return Response({"message": f"Missing fields: {', '.join(missing)}"}, status=400)

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            print("user created")
            return Response({"message": f"Student {student.name} added successfully"}, status=201)
        else:
            return Response(serializer.errors, status=400)

    #update a student's details 
    def update_student(self, request, id):
        student = get_object_or_404(Student, id=id)

        # Update User if needed
        user = student.user
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if username:
            user.username = username
        if password:
            user.set_password(password)  # make sure to hash
        if email:
            user.email = email
        user.save()

        # Update Student profile
        course_id = request.data.get("course")
        school_id = request.data.get("school")

        course = get_object_or_404(Course, id=course_id) if course_id else student.course
        school = get_object_or_404(School, id=school_id) if school_id else student.school

        data = {
            "name": request.data.get("name", student.name),
            "phone_number": request.data.get("phoneNumber", student.phone_number),
            "course": course.id,
            "school": school.id,
            "grade": request.data.get("grade", student.grade),
            "user": student.user.id
        }

        serializer = StudentSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"{data['name']} updated successfully"}, status=200)
        else:
            return Response(serializer.errors, status=400)


    #show the student details for a specific student 
    def show_student_details(self, request, id, instance=None): 
        student = get_object_or_404(Student, id=id)
        student_serializer = StudentSerializer(student)
        return Response({"student": student_serializer.data}, status=status.HTTP_200_OK)
    
    #show all students for a specific school 
    def show_all_students_by_school(self, request, id, instance=None): 
        school = get_object_or_404(School, id=id)
        students = Student.objects.filter(school=school)
        students_serializer = StudentSerializer(students, many=True)
        return Response({"students": students_serializer.data}, status=status.HTTP_200_OK)
    
    #show all students 
    def show_all_students(self, request, id=None, instance=None): 
        students= Student.objects.all()
        students_serializer = StudentSerializer(students, many=True)
        return Response({"students": students_serializer.data}, status=status.HTTP_200_OK)
    
    #delete student 
    def delete_student(self, request, id, instance=None): 
        return delete_element(Student, id)
    
    #show all the units for a specific student 
    def show_all_units_for_student(self, request, id, instance=None): 
        student = get_object_or_404(Student, id=id)
        units = Unit.objects.filter(course=student.course)
        serializer = UnitSerializer(units, many=True)
        return Response({"units" : serializer.data}, status=status.HTTP_200_OK) 
    