from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render,redirect,get_object_or_404
from authenticate.models import Profile
from jobcv.models import Cv,JobCircular
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

def registration(request):
    templates ='authenticate/registration.html'
    contex_password= {'error_pass':'Password Doesn\'t Match'}
    contex_user= {'user_error':'This Username or Email Alredy Taken'}
    if request.method == "POST":
        if request.POST['password']== request.POST['password2']:
            try:
                users= User.objects.get(username=request.POST['username'])
                email= User.objects.get(email=request.POST['email'])
                if users or email:
                    return render(request,templates,contex_user)
            except User.DoesNotExist:
                users= User.objects.create_user(request.POST['username'],email=request.POST['email'], password=request.POST['password'])
                auth.login(request, users)
                return redirect('profile')

        else:
            return render(request,templates,contex_password)
    else:
        return render(request,templates)



def login (request):
    contex_error={'error_user':'Username or Password Is Incorrect'}
    templates= 'authenticate/login.html'

    if request.method=="POST":
        user =auth.authenticate(username= request.POST['username'], password= request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request,templates,contex_error)
    else:
        return render(request,templates)

@login_required
def logout (request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('home')

@login_required
def create_profile (request):
    templates= 'authenticate/create_profile.html'
    context={'id':'This ID alredy exist'}
    if request.method== 'POST' and request.FILES['image']:

        post=Profile()
        try:
            id_test =Profile.objects.get(versity_id_number=request.POST['id'])
            if id_test:
                return render(request,templates,context)
        except Profile.DoesNotExist:
             post.versity_id_number=request.POST.get('id')


        post.full_name= request.POST.get('fullname')
        post.email= request.POST.get('email')
        post.image=request.FILES['image']
        post.user=request.user
        post.skill=request.POST.get('skill')
        post.facebook=request.POST.get('facebook')
        post.github=request.POST.get('github')
        post.linkedin=request.POST.get('linkedin')
        post.page_permission= 1
        post.save( )

        return redirect('home')
    else:
        return render(request,templates)

def editprofile(request):
    templates= 'authenticate/create_profile.html'
    context={'id':'This ID alredy exist','phone':'This Number alredy exist'}
    if request.method== 'POST' or request.FILES['image']:

        post=Profile()
        try:
            id_test =Profile.objects.get(versity_id_number=request.POST['id'])
            if id_test:
                return render(request,templates,context)
        except Profile.DoesNotExist:
             id=post.versity_id_number=request.POST.get('id')

        try:
            phone_test =Profile.objects.get(mobile_number=request.POST['phone'])
            if phone_test:
                return render(request,templates,context)
        except Profile.DoesNotExist:
             number=post.mobile_number=request.POST.get('phone')

        first_name= request.POST.get('firstname')
        last_name= request.POST.get('lastname')
        full_name= first_name+' '+last_name

        name=post.full_name= full_name
        email=post.email= request.POST.get('email')
        batch=post.batch=request.POST.get('batch')
        gender=post.gender=request.POST.get('gender')
        age=post.age=request.POST.get('age')

        image=post.image=request.FILES['image']

        work=post.working=request.POST.get('working_side')
        skill= post.skill=request.POST.get('skill')
        facebook=post.facebook=request.POST.get('facebook')
        github=post.github=request.POST.get('github')
        linkedin=post.linkedin=request.POST.get('linkedin')
        page=post.page_permission= 1

        Profile.objects.filter(user = request.user).update(full_name=name, email=email,versity_id_number=id,mobile_number=number, batch=batch,gender=gender,age=age,image=image,working=work,skill=skill,facebook=facebook,github=github,linkedin=linkedin,page_permission=page)

        return redirect('home')
    else:
        return render(request,templates)

@login_required
def show_profile (request,pk):
    templates= 'authenticate/show_profile.html'
    cv = Cv.objects.all()
    try:
        check_create_user_profile= get_object_or_404(Profile,user= request.user )

    except:
        return redirect('profile')
    ccup=check_create_user_profile.page_permission
    if ccup ==str(1):
        profile=Profile.objects.filter(user__pk=pk)
        try:
            p_name=profile.full_name
        except:
            p_name= request.user

        contex={'profile':profile,'p_name':p_name}
        return render(request,templates,contex)
    else:
        return redirect('profile')

@login_required
def edit_job_cv(request):

    templates= 'authenticate/edit.html'

    cv=Cv.objects.filter(user=request.user)
    job=JobCircular.objects.filter(user=request.user)

    if job and cv:
        context= {'userjob':job,'usercv':cv}
    elif not cv and not job:
        context={'joberror':'You have no any JOB','cverror':'You have no any CV'}
    elif job and not cv:
        context={'userjob':job,'cverror':'You have no any CV'}
    elif not job and cv:
        context={'usercv':cv,'joberror':'You have no any JOB'}
    return render(request,templates,context)

@login_required
def delete_job(request,pk):
    if request.method == 'POST':
        JobCircular.objects.get(pk=pk).delete()
    return redirect('edit_cv_job')

@login_required
def delete_cv(request,pk):
    if request.method == 'POST':
        Cv.objects.get(pk=pk).delete()
    return redirect('edit_cv_job')
