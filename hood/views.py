from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from .forms import AddProfileForm,AddBusinessForm,AddPostForm,ChangeLocationForm
from .models import Profile,Post,Business,Hood,Contact
from cloudinary.forms import cl_init_js_callbacks      
from .filters import BusinessFilter
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def homepage(request):
    hoods = Hood.objects.all()
    return render(request,'hood/home.html', {"hoods":hoods})

def about(request):
    return render(request,'hood/about.html')

@login_required(login_url='/accounts/login/')
def addprofile(request):
    current_user=request.user

    if request.method=="POST":
        form = AddProfileForm(request.POST,request.FILES)
        if form.is_valid():
           new_profile= form.save(commit=False)
           new_profile.user=current_user
           new_profile.save()
           return redirect('local')
    else:
        form=AddProfileForm()
    return render(request, 'hood/addprofile.html',{"form":form})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user=current_user)
    businesses = Business.objects.filter(owner=current_user)
    posts = Post.objects.filter(poster=current_user)
    return render(request,'hood/profile.html',{"current_user":current_user,"profile":profile,"businesses":businesses,"posts":posts})

@login_required(login_url='/accounts/login/')
def addbusiness(request):
    current_user=request.user

    if request.method=="POST":
        form=AddBusinessForm(request.POST)
        if form.is_valid():
            new_business=form.save(commit=False)
            new_business.owner=current_user
            new_business.save()
            return redirect('business')
    else:
        form=AddBusinessForm()
    return render(request,'hood/addbusiness.html',{"current_user":current_user,"form":form})

@login_required(login_url='/accounts/login/')
def business(request):
    businesses=Business.objects.all()
    return render(request,'hood/business.html', {"businesses":businesses})

@login_required(login_url='/accounts/login/')
def filterbusiness(request):
    if request is None:
        return Business.objects.none()
    filter_list = Business.objects.all()
    business_filter = BusinessFilter(request.GET, queryset=filter_list)
    return render(request,'hood/searchbusiness.html',{"filter":business_filter})

@login_required(login_url='/accounts/login/')
def posts(request,hood_id):
    hood=Hood.objects.get(id=hood_id)
    postups=hood.posts.all()
    return render(request, 'hood/postarea.html',{"hood":hood,"postups":postups})

@login_required(login_url='/accounts/login/')
def addpost(request,hood_id):
    hood = Hood.objects.get(id=hood_id)
    current_user=request.user
    form=AddPostForm()

    if request.method == 'POST':
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.area = hood
            new_post.poster=current_user
            new_post.save()
            return redirect('local')
        else:
            form=AddPostForm()
    return render(request, 'hood/addpost.html',{"form":form,"hood":hood,"current_user":current_user})

@login_required(login_url='/accounts/login/')
def hoodcontacts(request,hood_id):
    hood = Hood.objects.get(id=hood_id)
    contacters = hood.contacts.all()
    return render(request,'hood/contacts.html',{"hood":hood,"contacters":contacters})

@login_required(login_url='/accounts/login/')
def onlylocal(request):
    try:
        current_user=request.user
        userlocal=current_user.userprofle.hood
        # userlocal= Profile.objects.filter(hood=current_user.userprofle.hood)
        contacters=userlocal.contacts.all()
        businesses=userlocal.businesses.all()
        return render(request,'hood/local.html',{"userlocal":userlocal,"current_user":current_user,"contacters":contacters,"businesses":businesses})
    except ObjectDoesNotExist:
        return render(request, 'hood/noprofile.html')

@login_required(login_url='accounts/login/')
def changelocation(request):
    try:
        current_user=request.user

        if request.method=="POST":
            form = ChangeLocationForm(request.POST)
            if form.is_valid():
                new_location=form.cleaned_data['hood']
                new_area=Profile.objects.get(user=current_user)
                new_area.hood=new_location
                new_area.save()
                return redirect('local')

        else:
            form=ChangeLocationForm()
        return render(request, 'hood/changelocation.html',{"form":form})
    except ObjectDoesNotExist:
            return render(request, 'hood/noprofile.html')



            

# def addprofile(request):
#     home=form-cleaned_data(neighbourhood)
        # prohome=Hood.objects.get(name=home)
        # hood=prohome
