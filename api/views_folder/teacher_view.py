from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Teacher, School
from ..serializers import *
from ..utils import serializer_checker, delete_element


class TeacherView(APIView): 
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
            "show-specific-teacher" : self.show_specific_teacher, 
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
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"message": "Missing username or password"}, status=400)

        # Create User first
        user = User.objects.create_user(username=username, password=password, role="teacher")

        # Prepare serializer data including the user
        data = {
            "user": user.id,  # if your serializer expects a PK for the user
            "school": school.id,
            "phone_number": request.data.get("phoneNumber"),
            "name": request.data.get("name")
        }
        
        # Check required fields
        required_fields = ["name", "phone_number"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Teacher added successfully. "}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    # Update a teacher's details
    def update_teacher(self, request, id, instance=None): 
        teacher = get_object_or_404(Teacher, id=id)
        user = teacher.user

        # Update User fields if provided
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if username:
            user.username = username
        if password:
            user.set_password(password)  # hash password
        if email:
            user.email = email
        user.save()

        # Update Teacher profile fields
        school_id = request.data.get("school")
        school = get_object_or_404(School, id=school_id) if school_id else teacher.school

        data = {
            "name": request.data.get("name", teacher.name),
            "phone_number": request.data.get("phoneNumber", teacher.phone_number),
            "school": school.id,
            "user": teacher.user.id
        }

        serializer = TeacherSerializer(teacher, data=data, partial=True)
        return serializer_checker(serializer, f"{data['name']} updated successfully. ")

    
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
    def show_specific_teacher(self, request, id, instance=None): 
        teacher = get_object_or_404(Teacher, id=id)
        serializer = TeacherSerializer(teacher)
        return Response({"teacher" : serializer.data}, status=status.HTTP_200_OK)

    #delete teacher 
    def delete_teacher(self, request, id, instance=None): 
        return delete_element(Teacher, id)
