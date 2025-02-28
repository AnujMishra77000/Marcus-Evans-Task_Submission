from django.urls import path, include
from Management.api.views import  Booklist, CretaeBook, DeleteBook 

urlpatterns = [
    path('booklist/',Booklist.as_view(), name='Book-list'),
    path('<int:pk>/', CretaeBook.as_view(), name='Create-Book'), 
    path('<int:pk>/', DeleteBook.as_view(), name='Delete-Book'),  

]