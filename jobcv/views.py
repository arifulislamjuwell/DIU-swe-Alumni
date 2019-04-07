from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from authenticate.models import Profile
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
# Create your views here.

@login_required
def add_job(request):
    templates ='job/add_job.html'
    contex={'error_input':'You have to input all field with data'}

    try:
        check_create_user_profile= get_object_or_404(Profile,user= request.user )

    except:
        return redirect('profile')

    ccup=check_create_user_profile.page_permission
    if ccup ==str(1):

        if request.method == 'POST':
            post=JobCircular()
            post.user=request.user
            post.company= request.POST.get('company_name')
            post.post_name= request.POST.get('post_name')
            post.job_type=request.POST.get('job_type')
            post.qualification=request.POST.get('qualifications')
            post.skill=request.POST.get('skill_needed')
            post.website=request.POST.get('website')
            post.age_limit=request.POST.get('age_limit')
            post.job_nature=request.POST.get('job_nature')
            post.salary_range=request.POST.get('salary_range')
            post.save()

            return redirect('home')

        else:
            return render(request,templates,contex)

    else:
        return redirect('profile')


def job_circular_list(request):
    templates= 'job/job_circular_list.html'
    job_circular= JobCircular.objects.all()
    job=job_circular.filter(approve='a')
    query=request.GET.get('q')
    if query:
        job= job.filter(
            Q(skill__icontains=query)|
            Q(job_type__icontains=query)|
            Q(company__icontains=query)
        ).distinct()
    contex= {'job':job}
    return render(request,templates,contex)

def job_circular_details(request, slug):
    templates= 'job/job_details.html'
    job= get_object_or_404(JobCircular, slug=slug)
    contex= {'job':job}
    return render(request,templates,contex)

@login_required
def upload_cv(request):
    templates= 'cv/add_cv.html'
    catagories= CvCatagory.objects.all()
    contex ={'catagory':catagories}
    try:
        check_create_user_profile= get_object_or_404(Profile,user= request.user )

    except:
        return redirect('profile')
    ccup=check_create_user_profile.page_permission
    if ccup ==str(1):

        if request.method == 'POST' and request.FILES['upload_file']:
            post=Cv()
            position=request.POST.get('position')
            catagory= get_object_or_404(CvCatagory, name=position)
            post.catagory= catagory
            post.user= request.user
            post.skill= request.POST.get('skill')
            post.email= request.POST.get('email')
            post.file= request.FILES['upload_file']
            post.save()

            return redirect('home')
        else:
            return render(request,templates,contex)
    else:

        return redirect('profile')

def add_cv_catagory(request):
    if request.method=='POST':
        catagory=CvCatagory()
        catagory.name=request.POST.get('cvc')
        catagory.save()
        return redirect('add_cv')

def cv_catagory_list(request):
    templates= 'cv/cv_catagory_list.html'
    catagory= CvCatagory.objects.all()
    contex = {'cvcatagory':catagory}
    return render(request,templates,contex)

def req_cv(request,pk):
    catagory= get_object_or_404(CvCatagory,pk=pk)
    cvs=Cv.objects.all().filter(catagory=catagory)
    request_cv=Request_cv()
    request_cv.catagory=catagory
    request_cv.user=request.user
    request_cv.check=1
    request_cv.save()
    for cv in cvs:
        obj=Requested_feedback_cv()
        obj.request_user=request.user.username
        obj.cv_user=cv.user.username
        obj.tour=catagory.name
        obj.email=cv.email
        obj.skill=cv.skill
        obj.save()

    return redirect('cv_catagory')

@login_required
def cv_catagory_post_list(request,slug):
    templates= 'cv/catagory_post_list.html'
    catagories = CvCatagory.objects.all()
    cv = Cv.objects.all()
    if slug:
        catagory= get_object_or_404(CvCatagory, slug=slug)
        cv= cv.filter(catagory = catagory, approve ='a').count()

    req= Request_cv.objects.all().filter( user= request.user, catagory=catagory)
    contex ={'catagories':catagories, 'cv':cv, 'catagory':catagory,'req':req}
    return render(request,templates,contex)

def requested_cv_feedback(request):
    templates= 'cv/requested_cv.html'
    feedback= Requested_feedback_cv.objects.all().filter(request_user=request.user.username,approve='a')
    if not feedback:
        no_feed= 'Admin not permit yet'
        context={'no':no_feed}
        return render(request,templates,context)
    context={'feed':feedback}
    return render(request,templates,context)


