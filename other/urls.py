
from django.urls import path
from . import views
urlpatterns = [
    path ('',views.home, name='home'),
    path ('announcement/',views.announcement,name='announcement'),
    path ('contact-us/',views.contact_us,name='contact'),
    path ('gallery/',views.gallery, name= 'gallery'),
    path ('Ariful-Islam-Juwel/',views.aijuwel, name='juwel'),
]
