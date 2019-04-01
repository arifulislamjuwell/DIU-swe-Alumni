from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name =models.CharField(max_length=100,blank=True)
    email=models.EmailField(max_length=200,blank=True)
    versity_id_number= models.CharField(max_length=20, blank=True)
    image= models.FileField(upload_to='profile/')
    skill=models.CharField(max_length=200,blank=True)
    facebook=models.CharField(max_length=200,blank=True)
    github=models.CharField(max_length=300,blank=True)
    linkedin= models.CharField(max_length=200,blank=True)
    page_permission=models.CharField(max_length=5,blank=True)

    def __str__(self):
        return self.full_name
