from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('librarian', 'Librarian'),
    ]
    role = models.CharField(max_length=20, choices= ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(Group, related_name="management_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="management_user_permissions", blank=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
    
class Book(models.Model):
    title=models.CharField(max_length=100, unique=True)
    author=models.CharField(max_length=50)
    genre=models.CharField(max_length=100)
    book_count=models.IntegerField(default=5)
    availability=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Borrower(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    borrowed_date=models.DateTimeField(auto_now_add=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE, related_name="Borrower")
    due_date=models.DateTimeField(default=None)
    return_date=models.DateTimeField(null=True, blank=True)
    return_status=models.BooleanField(default=True)


    def __str__(self):
       return f"{self.user_name.username} borrowed '{self.book.title}'"

    



 

