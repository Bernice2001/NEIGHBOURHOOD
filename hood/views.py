from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from .forms import *
from .models import *
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')
    
def info(request):
    return render(request, 'info.html')

def new_account(request, username):
    user = request.user
    hood = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST)
        profile = ProfileForm(request.POST)
        if form.is_valid() and profile.is_valid():
            response = form.save()
            data = profile.save(commit=False)
            data.user = user
            profile.hood = response
            profile.save()
            return redirect('/')
    else:
        form = NeighbourhoodForm()
        profile = ProfileForm()
    
    return render(request, 'new_hood.html', {'profile':ProfileForm, 'form':NeighbourhoodForm})

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

