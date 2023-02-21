from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile
from posts.models import Post
from django.contrib import messages
from posts.forms import CommentForm

# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome {user.username}, you are logged in')
                return redirect('feed')
            else:
                messages.error(request,f"Invalid username or password")
        else:
            messages.error(request,f"Invalid username or password")
    form = LoginForm()
    return render(request,'users/login.html',{'form':form})

@login_required
def index(request):
    current_user=request.user
    profile=Profile.objects.filter(user=current_user).first()
    posts=Post.objects.filter(user=current_user).order_by("-created")
    return render(request,'users/index.html',{'posts':posts,'profile':profile})

def register(request):
    if request.method=="POST":
        user_form=UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request,f'Registered Successfully')
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    user_form=UserRegistrationForm()
    return render(request,'users/register.html',{'user_form':user_form})
    
@login_required
def edit(request):
    if request.method=="POST":
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.info(request,f'Profile updated successfully')
            return redirect('profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)

    return render(request,'users/edit.html',{'user_form':user_form,'profile_form':profile_form})

@login_required
def profile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    posts=Post.objects.filter(user=user).order_by("-created")
    return render(request,'users/profile.html',{'profile':profile,'posts':posts})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,f'You have been logged out')
    return redirect('login')


