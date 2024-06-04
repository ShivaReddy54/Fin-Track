from django.db import models

class Accounts(models.Model):
    full_name = models.CharField(max_length=100)
    date = models.DateField()
    no_of_pages = models.IntegerField()
    page_amounts = models.TextField(default='')  # Default empty dictionary

class Comments(models.Model):
    name = models.CharField(max_length=100)
    mobil = models.CharField(max_length=15)
    comment = models.TextField(default='')

