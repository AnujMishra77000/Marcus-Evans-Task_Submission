from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from datetime import timedelta

class Book(models.Model):
    title=models.CharField(max_length=100, unique=True)
    author=models.CharField(max_length=50)
    genre=models.CharField(max_length=100)
    availability=models.BooleanField(default=True)

    def __str__(self):
        return self.title
    

class Borrower(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    purchages_date=models.DateTimeField(auto_now_add=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE, related_name="Borrower")
    due_date=models.DateTimeField(default=None)

    def set_due_date(sender, instance, **kwargs):
      if not instance.due_date:
         instance.due_date = instance.purchases_date + timedelta(days=7)

    def __str__(self):
       return str(self.user_name) + " | " + self.purchages_date + " | " + str(self.book)

    



 

