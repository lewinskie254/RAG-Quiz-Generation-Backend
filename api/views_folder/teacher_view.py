from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Teacher, School
from ..serializers import *
from ..utils import serializer_checker, delete_element


class SchoolView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-teacher": self.add_new_teacher,
            "update-teacher" : self.update_teacher, 
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
            "show-all-teachers": self.show_all_teachers,
            "show-teachers-by-school" : self.show_teachers_by_school, 
            "show-specific-teachers" : self.show_specific_teachers, 
            "delete-teacher" : self.delete_teacher, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    

    #Add A New Teacher
    def add_new_teacher(self, request, id=None, instance=None): 
        school = get_object_or_404(School, id=request.data.get("school"))

        data = {
            "name" : request.data.get("name"),  
            "phone_number" : request.data.get("phone_number"), 
            "school" : school
        }

        required_fields = ["name", "phone_number"]
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
     
        serializer = TeacherSerializer(data=data) 
        return serializer_checker(serializer, f"{data['name']} added successfully") 
    
    #update a teacher's details
    def update_teacher(self, request, id, instance=None): 
        teacher = get_object_or_404(Teacher, id=id)
        school_id = request.data.get("school")
        school = get_object_or_404(School, id=school_id) if school_id else teacher.school

        data = {
            "name" : request.data.get("name") or teacher.name,  
            "phone_number" : request.data.get("phone_number") or teacher.phone_number, 
            "school" : school 
        }
     
        serializer = TeacherSerializer(teacher, data=data, partial=True) 
        return serializer_checker(serializer, f"{data['name']} updated successfully") 
    
    #show all teachers  
    def show_all_teachers(self, request, id=None, instance=None): 
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response({"teachers" : serializer.data}, status=status.HTTP_200_OK)
    
    #fetch teacher by school 
    def show_teachers_by_school(self, request, id, instance=None): 
        teachers = Teacher.objects.filter(school=id)
        serializer = TeacherSerializer(teachers, many=True)
        return Response({"teachers" : serializer.data}, status=status.HTTP_200_OK)

    #fetch a specific teacher 
    def show_specific_teachers(self, request, id, instance=None): 
        teacher = get_object_or_404(Teacher, id=id)
        serializer = TeacherSerializer(teacher)
        return Response({"teacher" : serializer.data}, status=status.HTTP_200_OK)

    #delete teacher 
    def delete_teacher(self, request, id, instance=None): 
        return delete_element(Teacher, id)
