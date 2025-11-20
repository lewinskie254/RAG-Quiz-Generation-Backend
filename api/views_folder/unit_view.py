from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Course, Teacher
from ..serializers import *
from ..utils import serializer_checker, delete_element


class UnitView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "add-unit": self.add_new_unit,
            "update-unit" : self.update_unit, 
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
            "show-all-units": self.show_all_units,
            "show-units-by-teacher" : self.show_units_by_teacher, 
            "show-specific-unit" : self.show_specific_unit, 
            "delete-unit" : self.delete_unit, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    #add a new unit 
    def add_new_unit(self, request, id=None, instance=None): 
        course_id = request.data.get("course")
        teacher_id = request.data.get("teacher")

        if not course_id:
            return Response({"message": "Missing course"}, status=status.HTTP_400_BAD_REQUEST)

        if not teacher_id:
            return Response({"message": "Missing teacher"}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        teacher = get_object_or_404(Teacher, id=teacher_id)

        data = {
            "course": course,
            "teacher": teacher,
        }

        score_str = request.data.get("score")
        if score_str:
            try:
                data["total_score"] = int(score_str)
            except (TypeError, ValueError):
                return Response(
                    {"message": "total score must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = UnitSerializer(data=data)
        return serializer_checker(serializer, "Unit added successfully")

    #update unit 
    def update_unit(self, request, id, instance=None): 
        unit = get_object_or_404(Unit, id=id)

        course_id = request.data.get("course")
        teacher_id = request.data.get("teacher")

        course = get_object_or_404(Course, id=course_id) if course_id else unit.course
        teacher = get_object_or_404(Teacher, id=teacher_id) if teacher_id else unit.teacher

        data = {
            "course": course,
            "teacher": teacher,
        }

        score_str = request.data.get("score")
        if score_str is not None:
            try:
                data["total_score"] = int(score_str)
            except (TypeError, ValueError):
                return Response(
                    {"message": "Score must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else: 
            data["total_score"] = unit.total_score
        
        serializer = UnitSerializer(unit, data=data, partial=True)
        return serializer_checker(serializer, "unit updated successfully")

    #show all units 
    def show_all_units(self, request, id=None, instance=None): 
        units  = Unit.objects.all()
        serializer = UnitSerializer(units, many=True)
        return Response({"units" : serializer.data}, status=status.HTTP_200_OK)
    
    #show all units taught by a specific teacher 
    def show_units_by_teacher(self, request, id, instance=None): 
        units = Unit.objects.filter(teacher_id=id) 
        serializer = UnitSerializer(units, many=True)
        return Response({"units" : serializer.data}, status=status.HTTP_200_OK)

    #show specific unit 
    def show_specific_unit(self, request, id, instance=None): 
        unit = get_object_or_404(Unit, id=id)
        serializer = UnitSerializer(unit)
        return Response({"unit" : serializer.data}, status=status.HTTP_200_OK)

    #delete unit 
    def delete_unit(self, request, id, instance=None): 
        return delete_element(Unit, id)