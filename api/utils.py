from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

def serializer_checker(serializer, success_msg=None):
    if serializer.is_valid():
        serializer.save()
        msg = success_msg or "Created successfully"
        return Response({"message": msg}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def delete_element(model, id):
    instance = get_object_or_404(model, id=id)
    instance.delete()
    return Response({"message": f"{model.__name__} {id} deleted"}, status=status.HTTP_200_OK)