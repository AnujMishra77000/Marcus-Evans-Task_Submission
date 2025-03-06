from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from Management.api import serializers 
from Management.models import Book, Borrower
from datetime import timedelta
from django.utils.timezone import now
from .permissions import IsUser, IsLibrarian
from django.shortcuts import get_object_or_404


class Booklist(generics.ListAPIView):
    serializer_class = serializers.BookSerializer
    def get(self, request):
        data = Book.objects.all()
        serializer = serializers.BookSerializer(data, many=True)
        return Response(serializer.data)   


class CretaeBook(APIView):
    permission_classes = [IsLibrarian]

    def post(self, request): #Function to create a new book inside library DB.
        title= request.data.get('title')
        if Book.objects.filter(title=title).exists():
            return Response({"error":"Book is already exists with same Ttile name"})
        
        serializer = serializers.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def put(self, request, pk): #To Update a book which is already presents inside.
        data = Book.objects.get(pk=pk)
        serializer = serializers.BookSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
          
    def delete(self, request, pk):# function to delete the exists book inside library DB.
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message":"Book deleted Successfully"})
        except Book.DoesNotExist:
            return Response({"error":"Book not found"}, status=status.HTTP_404_NOT_FOUND)

class Boorowerlist(generics.ListAPIView):
    permission_classes=[IsLibrarian]
    serializer_class = serializers.BorrowerSerializer
    def get(self, request):
        data = Borrower.objects.all()
        serializer = serializers.BorrowerSerializer(data, many=True)
        return Response(serializer.data)   

class BorrowBook(APIView):
    permission_classes=[permissions.IsAuthenticated, IsUser]

    def post(self, request):
        user = request.user
        book_id = request.data.get("book")

        book = get_object_or_404(Book, id=book_id)

        if Borrower.objects.filter(user_name=user, book=book, return_status = False).exists():
            return Response({"error": f"You Already Borrowed this Book: {str(book)}"}, status=status.HTTP_400_BAD_REQUEST)

        if book.book_count <=0:
            return Response({"error":"Book is not available."}, status=status.HTTP_400_BAD_REQUEST)
        
        borrow = Borrower.objects.create(
            user_name=user,
            book=book,
            due_date= now() + timedelta(days=7),
            return_status=False

        )
        serializers_borrow= serializers.BorrowerSerializer(borrow)

        book.book_count -= 1
        if book.book_count == 0:
            book.availability = False
        book.save()

        
        return Response(serializers_borrow.data,status=status.HTTP_201_CREATED )

class BookReturn(APIView):
    permission_classes=[permissions.IsAuthenticated, IsUser]

    def post(self, request):
        user = request.user
        book_id = request.data.get("book")
        
        borrow = Borrower.objects.filter(user_name=user, book_id=book_id, return_status=False).first()
        if not borrow:
          return Response({"error": "No active borrowing record for this book."},status=status.HTTP_400_BAD_REQUEST)
        
        
        book = get_object_or_404(Book, id=book_id)
       
        book.book_count += 1
        borrow.return_status = True
        borrow.return_date = now() + timedelta() 

        book.save()
        borrow.save()

        return Response({"meesage":"Book returned successfully.","Return_Status": borrow.return_status}, status=status.HTTP_200_OK)

class BorrowHistoryView(APIView):
    permission_classes=[permissions.IsAuthenticated, IsUser]
    
    def get(self, request):
        user=request.user
        borrow_history =  Borrower.objects.filter(user_name=user)

        serializer = serializers.BorrowerSerializer(borrow_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ActiveBorrowed(APIView): 
    permission_classes=[permissions.IsAuthenticated, IsUser]   
    def get(self, request):
        user=request.user

        active_borrows= Borrower.objects.filter(user_name=user, return_status= False)

        
        if not  active_borrows:
            return Response ({"meesgae":"No Active Borrowed Book available."})
        
        serializer = serializers.BorrowerSerializer(active_borrows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)