from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, Teacher
from ..serializers import *


class CourseView(APIView):
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-course": self.add_new_course,
            "update-course" : self.update_course, 
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
            "show-all-school": self.show_all_schools,
            "show-specific-school" : self.show_specific_school, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    

    #Add A New Course 