from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course
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
    def add_new_course(self, request, id=None, instance=None): 
        data = {
        "name": request.data.get("name"), 
        "units": request.data.get("units")  # keep as string first
        }

        required_fields = ["name", "units"]
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Ensure units is an integer and handle errors
        try:
            data["units"] = int(data.get("units", 0))
        except (TypeError, ValueError):
            return Response({"message": "Units must be a number"}, status=status.HTTP_400_BAD_REQUEST)



        serializer = CourseSerializer(data=data) 
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message" : f"{data['name']} course added successfully"}, 
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)