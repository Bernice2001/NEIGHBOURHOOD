from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from .forms import ProfileForm,BusinessForm,PostForm,UpdateForm,ChangeHood
from .models import Profile,Businesses,Neighbour,Feeds
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')
    
def info(request):
    return render(request, 'info.html')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    return render(request, '/django_registration/login.html')
 
@login_required
def logout(request):
    django_logout(request)
    return  redirect(request, '/')   

@login_required(login_url='/accounts/login/')
def profile(request):
    profile=Profile.objects.filter(user=request.user)
    bizz=Businesses.objects.filter(user=request.user)
    post=Feeds.objects.filter(user=request.user)
    if request.method=='POST':
        instance=Profile.objects.get(user=request.user)
        form=UpdateForm(request.POST or None,request.FILES,instance=instance)
        if form.is_valid():
            upda=form.save(commit=False)
            upda.save()


        return redirect('profile')
    else:
        form=UpdateForm()

    if request.method=="POST":
        instance=Profile.objects.get(user=request.user)
        change=ChangeHood(request.POST  or None,request.FILES,instance=instance)
        if change.is_valid():
            chan=change.save(commit=False)
            chan.save()
        return redirect('profile')
    else:
        change=ChangeHood()

    title='Profile'
    return render(request,'profile.html',{'profile':profile,"busi":busi,'post':post,"form":form,'title':title,'change':change})
@login_required(login_url='/accounts/login/')
def edit(request):

    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
        return redirect("profile")
    else:

        form=ProfileForm()

    title="Edit"
    return render(request,'edit.html',{'form':form,'title':title})
@login_required(login_url='/accounts/login/')
def business(request):
    if request.method=='POST':
        form=BusinessForm(request.POST)
        if form.is_valid():
            bizz=form.save(commit=False)
            bizz.user=request.user
            form.save()
        return redirect('profile')

    else:
        form=BusinessForm()
    return render(request,'business.html',{'form':form})
@login_required(login_url='/accounts/login/')
def feeds(request):

    try:

        profile=Profile.objects.filter(user=request.user)
        arr=[]
        for i in profile:
            arr.append(i.neigbor.id)

        id=arr[0]
        business=Businesses.objects.filter(neigbor=id)
        feed=Feeds.objects.filter(neigbor=id)
        pop_count=Profile.objects.filter(neigbor=id)
        all_hoods=Neighbour.objects.filter(id=id)
    except Exception as e:
        raise  Http404()

    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.neigbor=Neighbour(id)
            post.save()
        return redirect('feeds')
    else:
        form=PostForm()
    title='Feeds'

    return render(request,"feeds.html",{"business":business,'form':form,'feed':feed,'hoods':all_hoods,'title':title,'pop':pop_count ,'profile':profile})

@login_required(login_url='/accounts/login/')
def search(request):
    if 'businessesName' in request.GET and request.GET['businessesName']:
        name=request.GET.get('businessesName')
        results=Businesses.search_business(name)

        return render(request,'search.html',{'business':results,'name':name})
 