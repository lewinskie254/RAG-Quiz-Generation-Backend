from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, Student, School

class StudentView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-student": self.add_new_student,
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
            "add-main-user-update": self.add_temp_main_user,
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    def add_new_student(self, request): 
        course = get_object_or_404(Course, id=request.data.get("course"))
        school = get_object_or_404(School, id=request.data.get("school"))

        data = {
            "name" : request.data.get("student_name"), 
            "email" : request.data.get("email", ""), 
            "phone_number": request.data.get("phone_number"), 
            "course" : course.id, 
            "school" : school.id, 
            "grade" : 0 
        }
