from django.shortcuts import render, redirect
from rest_framework.views import APIView,Response
from .serializers import CommetsSerializers
from .models import Comments
from django.http import JsonResponse
from rest_framework.exceptions import NotFound
from rest_framework import status
# Create your views here.


class CommentApiView(APIView):

    def get_object(self, id):
        try:
            return Comments.objects.get(id == id)
        except:
            raise NotFound()

    def get(self, request):
        return Response(CommetsSerializers(Comments.objects.all(), many=True).data)

    def post(self, request):
        serializer = CommetsSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_comment(request,movie_slug):
    return redirect(request.META.get('HTTP_REFERER'))