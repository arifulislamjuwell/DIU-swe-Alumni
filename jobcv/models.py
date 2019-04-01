from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import datetime
# Create your models here.

class JobCircular(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    company= models.CharField(max_length=50, blank=False)
    slug= models.SlugField(unique=True, blank=True)
    post_name= models.CharField(max_length=50, blank=True)
    publication_Date=models.DateField(auto_now_add=True)
    job_type=models.CharField(max_length=100)
    qualification= models.CharField(max_length=15)
    skill= models.CharField(max_length=150)
    website= models.URLField(max_length=400, blank=True)
    age_limit=models.CharField(blank=True, max_length=10)
    job_nature=models.CharField(max_length=9)
    application_last_date=models.DateField(auto_now_add=True, blank=True, null=True)
    salary_range=models.CharField(max_length=10)

    APPROVE= (
        ('a', 'approve'),
        ('d', 'deny')

    )
    approve = models.CharField(choices=APPROVE,max_length=1, default='d')
    def __str__(self):
        return str(self.company)

    def _get_unique_slug(self):
        slug = slugify(self.company)
        unique_slug = slug
        num = 1
        while JobCircular.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('job_details', args=[self.slug])


class CvCatagory(models.Model):
    name= models.CharField(max_length=200)
    slug= models.SlugField(unique=True, blank=True)

    class Meta:
        ordering= ('name',)
        verbose_name= "catagory"
        verbose_name_plural='catagories'
    def __str__(self):
        return str(self.name)
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while CvCatagory.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cv_catagory_post', args=[self.slug])


class Cv(models.Model):
    catagory=models.ForeignKey(CvCatagory, on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    email=models.EmailField(max_length=200)
    skill= models.CharField(max_length=300)
    publish_date= models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='cv/')

    APPROVE= (
        ('a', 'approve'),
        ('d', 'deny')

    )
    approve = models.CharField(choices=APPROVE,max_length=1, default='d')
    def __str__(self):
        return str(self.skill)
class Request_cv(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    catagory=models.ForeignKey(CvCatagory,on_delete=models.CASCADE)
    check =models.CharField(max_length=1)
    APPROVE= (
        ('a', 'approve'),
        ('d', 'deny')

    )
    approve = models.CharField(choices=APPROVE,max_length=1, default='d')
