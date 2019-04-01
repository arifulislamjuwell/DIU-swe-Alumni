from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Sociallink(models.Model):
    name= models.CharField(max_length=100)
    link=models.URLField(max_length=300, blank=True)


class Annoucement(models.Model):
    title=models.CharField(max_length=200)
    location=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now=False)
    description=models.CharField(max_length=300)
    image=models.ImageField(upload_to='announcement/')

class Seminar(models.Model):
    image= models.FileField(upload_to='seminar/')
    title=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    description=models.CharField(max_length=300)
    time=models.DateTimeField(auto_now=False)


class Gallery_image_catagory(models.Model):
    name=models.CharField(max_length=15)

    def __str__(self):
        return str(self.name)


class Galarry_image(models.Model):
    catagory=models.ForeignKey(Gallery_image_catagory, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    image=models.FileField(upload_to='gallery_photo/')

class Contact_Us(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email=models.EmailField(max_length=200)
    subject=models.CharField(max_length=200)
    message= models.CharField(max_length=1000)
