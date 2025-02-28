from rest_framework import serializers
from Management.models import Book, Borrower
class BookSerializer(serializers.ModelSerializer):
    class Meta:
         model= Book
         fields='__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
         model= Borrower
         fields='__all__'         