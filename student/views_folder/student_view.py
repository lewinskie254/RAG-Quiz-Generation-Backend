from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, Student, School
from ..serializers import *

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
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    def add_new_student(self, request, id=None, instance=None): 
        course = get_object_or_404(Course, id=request.data.get("course"))
        school = get_object_or_404(School, id=request.data.get("school"))
        
        data = {
            "name": request.data.get("student_name"), 
            "email": request.data.get("email", ""), 
            "phone_number": request.data.get("phone_number"), 
            "course": course,   # Pass instance if serializer expects it
            "school": school,   # Pass instance if serializer expects it
            "grade": 0 
        }

        required_fields = ["name", "phone_number", "course", "school"]
        missing_fields = [key for key in required_fields if not data.get(key)]
        if missing_fields:
            return Response({"message": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        student_serializer = StudentSerializer(data=data)
        if student_serializer.is_valid(): 
            student_serializer.save()
            return Response({"message": f"{data['name']} saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_student(self, request, id):
        student = get_object_or_404(Student, id=id)

        # Optional updates
        course_id = request.data.get("course")
        school_id = request.data.get("school")

        course = get_object_or_404(Course, id=course_id) if course_id else student.course
        school = get_object_or_404(School, id=school_id) if school_id else student.school

        data = {
            "name": request.data.get("student_name", student.name),
            "email": request.data.get("email", student.email),
            "phone_number": request.data.get("phone_number", student.phone_number),
            "course": course,
            "school": school,
            # DON’T override grade unless needed
            "grade": request.data.get("grade", student.grade),
        }

        serializer = StudentSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"{data['name']} updated successfully"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def show_student_details(self, request, id, instance=None): 
        student = get_object_or_404(Student, id=id)
        student_serializer = StudentSerializer(student)
        return Response({"student": student_serializer.data}, status=status.HTTP_200_OK)
    
