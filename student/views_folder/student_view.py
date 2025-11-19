from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


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
        ...