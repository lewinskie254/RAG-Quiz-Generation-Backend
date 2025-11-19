from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import School
from ..serializers import *


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
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f'{data["name"]} created successfully'},
                status=status.HTTP_201_CREATED
            )

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f'{data["name"]} updated successfully'},
                status=status.HTTP_200_OK
            )

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
