from rest_framework import serializers
from Management.models import Book, Borrower
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
         model= Book
         fields='__all__'

class BorrowerSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source="user_name.username", read_only=True) 
    book = serializers.CharField(source="book.title", read_only=True) 
    borrowed_date = serializers.DateTimeField(format="%d-%b-%Y")
    due_date = serializers.DateTimeField(format="%d-%b-%Y", allow_null=True)
    return_date = serializers.DateTimeField(format="%d-%b-%Y", allow_null=True)


    class Meta:
        model = Borrower
        fields ='__all__'
    
   