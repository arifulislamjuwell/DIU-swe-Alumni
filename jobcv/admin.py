from django.contrib import admin

from . models import *
# Register your models here.
admin.site.register(JobCircular)
admin.site.register(CvCatagory)
admin.site.register(Cv)
admin.site.register(Request_cv)
admin.site.register(Requested_feedback_cv)
