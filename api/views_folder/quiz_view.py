from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Quiz, Question, Choices, StudentUnitScore, Unit
from ..serializers import *
from ..utils import serializer_checker, delete_element


class QuizView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "create-quiz": self.add_new_quiz,
            "update-quiz" : self.update_quiz, 
            "add-question": self.add_new_question, 
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
            "show-all-quizzes": self.show_all_quizzes,
            "show-specific-quiz" : self.show_specific_quiz, 
            "delete-quiz" : self.delete_quiz, 
        }
        func = actions.get(action)
        if not func:
            return Response(
                {"message": "invalid action"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return func(request, id=id, instance=instance)
    
    #add  a New Quiz 
    def add_new_quiz(self, request, id=None, instance=None): 
        unit = get_object_or_404(Unit, id=request.data.get("unit"))
        data = {
            "unit": unit, 
        }
        no_of_questions = request.data.get("number_of_questions", 0)
        if no_of_questions is not None: 
            try: 
                data["number_of_questions"] = int(no_of_questions)
            except (TypeError, ValueError):
                return Response(
                    {"message": "number_of_questions must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = QuizSerializer(data=data)
        if serializer.is_valid():
            quiz = serializer.save()  # Save returns the instance
            return Response({
                "message": "Quiz added successfully",
                "quiz_id": quiz.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_quiz(self, request, id, instance=None): 
        unit = get_object_or_404(Unit, id=request.data.get("unit"))
        data = {
            "unit": unit, 
        }
        no_of_questions = request.data.get("number_of_questions", 0)
        if no_of_questions is not None: 
            try: 
                data["number_of_questions"] = int(no_of_questions)
            except (TypeError, ValueError):
                return Response(
                    {"message": "number_of_questions must be a number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer = QuizSerializer(data=data)
        return serializer_checker(serializer, f"f{data['']}")