from rest_framework.response import Response
from rest_framework import status

def serializer_checker(serializer, success_msg=None):
    if serializer.is_valid():
        serializer.save()
        msg = success_msg or "Created successfully"
        return Response({"message": msg}, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
