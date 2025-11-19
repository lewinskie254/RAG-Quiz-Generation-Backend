from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import School
from ..serializers import *
from ..utils import serializer_checker


class SchoolView(APIView):
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-school": self.add_new_school,
            "update-school" : self.update_school, 
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
    
    #add a new school to the database 
    def add_new_school(self, request, id=None, instance=None):
        data = {
            "name": request.data.get("name"),
            "email": request.data.get("email"),
            "phone_number": request.data.get("phone_number"),
            "location": request.data.get("location"),
        }

        required_fields = ["name", "email", "phone_number", "location"]
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SchoolSerializer(data=data)
        return serializer_checker(serializer, f"{data['name']} created successfully. ")
    
    #update school details 
    def update_school(self, request, id, instance=None): 
        school = get_object_or_404(School, id=id)

        data = {
            "name": request.data.get("name", school.name),
            "email": request.data.get("email", school.email),
            "phone_number": request.data.get("phone_number", school.phone_number),
            "location": request.data.get("location", school.location),
        }

        serializer = SchoolSerializer(school, data=data, partial=True)
        return serializer_checker(serializer, f"{data['name']} updated successfully. ")
    
    #show all schools 
    def show_all_schools(self, request, id=None, instance=None): 
        schools = School.objects.all()
        serializer = SchoolSerializer(schools, many=True)
        return Response({"schools" : serializer.data}, status=status.HTTP_200_OK)
    
    #show specific school 
    def show_specific_school(self, request, id, instance=None): 
        school = get_object_or_404(School, id=id)
        serializer = SchoolSerializer(school)
        return Response({"school" : serializer.data}, status=status.HTTP_200_OK)