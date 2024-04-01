from django.db import models


class Member(models.Model):
    member_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=128, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, null=True)


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True)
    genre = models.CharField(max_length=255, null=True)
    publisher = models.CharField(max_length=255, null=True)
    summary = models.CharField(max_length=255, null=True)


class Loan(models.Model):
    loan_id = models.IntegerField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField()
