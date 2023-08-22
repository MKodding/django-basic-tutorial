from django.shortcuts import render
from django.http import HttpResponse
from first_app.forms import UserForm, UserProfileInfoForm

#

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(req):
    dict_content = {'text' : 'Hello World!!!', 'number': '100'}
    return render(req, 'first_app/index.html', context= dict_content)

def other(req):
    return render(req, 'first_app/other.html')

def register(req):
    registered = False

    if req.method == "POST":
        user_form = UserForm(data=req.POST)
        profile_form = UserProfileInfoForm(data=req.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in req.FILES:
                profile.profile_pic = req.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()


    return render(req, 'first_app/registration.html', context={'user_form': user_form, 
                                                               'profile_form': profile_form,
                                                               'registered': registered })

def user_login(req):

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(req, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('YOUR Account is Inactive')
        else:
            print('Login failed')
            return HttpResponse("Invalid login details")
    else:
        return render(req, 'first_app/login.html')
    

@login_required    
def user_logout(req):
    logout(req)
    return HttpResponseRedirect(reverse('index'))