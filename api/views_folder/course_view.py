from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course
from ..serializers import *
from ..utils import serializer_checker


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
            "show-all-courses": self.show_all_courses,
            "show-specific-course" : self.show_specific_course, 
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
        return serializer_checker(serializer, f"{data['name']} added successfully") 
    
    #update a course's details 
    def update_course(self, request, id, instance=None): 
        course  = get_object_or_404(Course, id=id) 
        data = {
            "name": request.data.get("name") or course.name, 
            "units": request.data.get("units") or course.units, 
        }

        serializer = CourseSerializer(course, data=data, partial=True)
        return serializer_checker(serializer, f"{data['name']} updated successfully") 
    
    #show all courses 
    def show_all_courses(self, request, id=None, instance=None): 
        courses = Course.objects.all() 
        serializer = CourseSerializer(courses, many=True)
        return Response({"courses" : serializer.data}, status=status.HTTP_200_OK)

    #show specific course 
    def show_specific_course(self, request, id, instance=None): 
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course)
        return Response({"course": serializer.data}, status=status.HTTP_200_OK)