from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Management.api import permissions
from Management.api import serializers
from Management.models import Book, Borrower
from Management.api  import pagination


class Booklist(generics.ListAPIView):
    serializer_class = serializers.BookSerializer
    def get(self, request):
        movies = Book.objects.all()
        serializer = serializers.BookSerializer(movies, many=True)
        return Response(serializer.data)   
    


class CretaeBook(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def post(self, request):
        serializer = serializers.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def put(self, request, pk):
        movie = Book.objects.get(pk=pk)
        serializer = serializers.BookSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class DeleteBook(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    def delete(self, request, pk):
        movie = Book.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


