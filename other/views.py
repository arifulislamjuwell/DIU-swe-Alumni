from django.shortcuts import render,get_object_or_404
from .models import Sociallink,Annoucement,Seminar,Galarry_image,Gallery_image_catagory,Contact_Us
from jobcv.models import Cv,JobCircular
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    batch_number=29
    templates= 'home/index.html'

    seminar=Seminar.objects.order_by('-pk')[:3]
    announcement=Annoucement.objects.order_by("-pk")[:5]
    cv= Cv.objects.all().filter( approve ='a').count()
    job= JobCircular.objects.all().filter( approve ='a').count()

    facebook= get_object_or_404(Sociallink, name='facebook')
    youtube= get_object_or_404(Sociallink, name='youtube')
    twitter=get_object_or_404(Sociallink, name='twitter')
    linkedin=get_object_or_404(Sociallink, name='linkedin')

    contex={'batch':batch_number,'fb':facebook,'yt':youtube,'t':twitter,'li':linkedin,'ann':announcement,'seminars':seminar,'cv':cv,'job':job}
    return render(request,templates,contex)


def announcement(request):
    templates='announce.html'
    all= Annoucement.objects.all()
    context={'announce':all}

    return render(request,templates,context)

def contact_us(request):
    templates= 'home/contact.html'
    if request.method=='POST':
        user=get_object_or_404(User, username=request.user)
        email=user.email
        contact=Contact_Us()
        contact.user=request.user
        contact.email=email
        contact.subject=request.POST.get('subject')
        contact.message=request.POST.get('message')
        contact.save()
    return render(request,templates)

def gallery(request):
    templates= 'home/gallery.html'
    seminar=Galarry_image.objects.all().filter( catagory__pk=1)
    convocation=Galarry_image.objects.all().filter( catagory__pk=2)
    meet=Galarry_image.objects.all().filter( catagory__pk=5)
    tour=Galarry_image.objects.all().filter( catagory__pk=4)
    foundation=Galarry_image.objects.all().filter( catagory__pk=3)
    context={'sem':seminar,'con':convocation,'meet':meet,'tour':tour,'fou':foundation}
    return render(request,templates,context)

def aijuwel(request):
    templates='aijuwel.html'
    return render(request,templates)
