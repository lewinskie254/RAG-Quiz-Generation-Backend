from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import Quiz, Question, Unit, Choice
from ..serializers import *
from ..utils import serializer_checker, delete_element


class QuizView(APIView): 
    def post(self, request, action, id=None, instance=None):
        actions = {
            "create-quiz": self.add_new_quiz,
            "update-quiz" : self.update_quiz, 
            "add-question": self.add_new_question, 
            "add-multiple-choice" : self.add_multiple_choice, 
            "update-multiple-choice" : self.update_multiple_choice, 
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
            "show-all-questions-per-quiz": self.show_all_questions_per_quiz, 
            "show-specific-quiz" : self.show_specific_quiz, 
            "show-specific-question": self.show_specific_question, 
            "show-multiple-choices-for-question" : self.show_multiple_choices_for_question, 
            "delete-quiz" : self.delete_quiz, 
            "delete-question" : self.delete_question, 
            "delete-multiple-choice" : self.delete_multiple_choice
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

    #update Quiz 
    def update_quiz(self, request, id, instance=None): 
        quiz = get_object_or_404(Quiz, id=id)
        unit_id = request.data.get("unit")
        unit = get_object_or_404(Unit, id=unit_id) if unit_id else quiz.unit

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
        else: 
            data["number_of_questions"] = quiz.number_of_questions
        serializer = QuizSerializer(quiz, data=data, partial=True)
        return serializer_checker(serializer, f"{quiz.id} updated successfully. ")
    
    #add new question 
    def add_new_question(self, request, id, instance=None): 
        quiz = get_object_or_404(Quiz, id=id)
        data = {
            "question" : request.data.get("question"), 
            "answer" : request.data.get("answer"), 
            "quiz" : quiz 
        }

        required_fields = ["question", "answer"]
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return Response(
                {"message": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            question = serializer.save()  # Save returns the instance
            return Response({
                "message": "Question added successfully",
                "question_id": question.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #show all quizzes 
    def show_all_quizzes(self, request, id=None, instance=None): 
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response({"quizzes": serializer.data}, status=status.HTTP_200_OK)
    
    #show all the questions per quiz 
    def show_all_questions_per_quiz(self, request, id, instance=None): 
        questions = Question.objects.filter(quiz=id)
        serializer = QuestionSerializer(questions, many=True)
        return Response({"questions": serializer.data}, status=status.HTTP_200_OK)

    #show specific quiz 
    def show_specific_quiz(self, request, id, instance=None): 
        quiz = get_object_or_404(Quiz, id=id)
        serializer = QuizSerializer(quiz)
        return Response({"quiz": serializer.data}, status=status.HTTP_200_OK)
    
    #get the specific question for the quiz 
    def show_specific_question(self, request, id, instance=None): 
        question = get_object_or_404(Question, id=id)
        serializer = QuestionSerializer(question)
        return Response({"question": serializer.data}, status=status.HTTP_200_OK)

    #delete quiz 
    def delete_quiz(self, request, id, instance=None): 
        return delete_element(Quiz, id)
    
    #delete question 
    def delete_question(self, request, id, instance=None): 
        return delete_element(Question, id)
    

    #add multiple choice answers for each question 
    def add_multiple_choice(self, request, id, instance=None): 
        question = get_object_or_404(Question, id=id)
        content = request.data.get("content")
        if content is None: 
            return Response({"message": "Missing content"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            "content" : content, 
            "question" : question
        }

        serializer = ChoiceSerializer(data=data)
        return serializer_checker(serializer, f"multiple choice for question {question.id} added")


    #update the multiple choice answer  
    def update_multiple_choice(self, request, id, instance=None): 
        choice = get_object_or_404(Choice, id=id) 
        question_id = request.data.get("question")
        question = get_object_or_404(Question, id=question_id) if question_id else choice.question
        content = request.data.get("content")
        data = {
            "content" : content or choice.content, 
            "question" : question 
        }
        serializer = ChoiceSerializer(choice, data=data, partial=True)
        return serializer_checker(serializer, f"{choice.id} updated successfully. ")
    
    #show the multiple choices for a question 
    def show_multiple_choices_for_question(self, request, id, instance=None): 
        question = get_object_or_404(Question, id=id)
        choices = Choice.objects.filter(question=question)
        serializer = ChoiceSerializer(choices, many=True)
        return Response({"choices": serializer.data}, status=status.HTTP_200_OK)
    
    #delete a multiple choice 
    def delete_multiple_choice(self, request, id, instance=None): 
        return delete_element(Choice, id)
