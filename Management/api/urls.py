from django.urls import path, include
from Management.api.views import  Booklist, CretaeBook, BorrowBook, Boorowerlist,BookReturn,BorrowHistoryView, ActiveBorrowed

urlpatterns = [
    path('booklist/',Booklist.as_view(), name='Book_list'),
    path('create/', CretaeBook.as_view(), name='Create_Book'), 
    path('update/<int:pk>/',CretaeBook.as_view(),name='update_book'),
    path('delete/<int:pk>/', CretaeBook.as_view(), name='Delete_Book'), 
    path('borrow/',BorrowBook.as_view(), name='borrow'),
    path('borlist/',Boorowerlist.as_view(), name='blist'),
    path('return/',BookReturn.as_view(), name='book_return'),
    path('history/', BorrowHistoryView.as_view(), name='Borrow_history'),
    path('active/',ActiveBorrowed.as_view(), name='active_book'),

]