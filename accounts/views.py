from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from verify_email.email_handler import send_verification_email
from .func import validate_email
from .forms import RegistrationForm

def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        email = request.POST.get("email")

        if password1 == password2:
            try:
                validate_password(password1)
            except ValidationError as exceptions:
                return render(request,"register.html",{"passwordError": exceptions, "length": len(list(exceptions))})
            else:
                if validate_email(email):
                    email_taken = User.objects.filter(email = email).exists()
                    username_taken = User.objects.filter(username = username).exists()
                    if email_taken:
                        message = "This email is already taken. Try again!"
                        return render(request,"register.html",{"emailExist":message})
                    elif username_taken:
                        message = "This username is already taken. Try again!"
                        return render(request,"register.html",{"usernameExist":message})
                    else:
                        form = RegistrationForm(request.POST)
                        inactiveUser = send_verification_email(request, form)
                        return redirect("accounts:registration_done")
                        
                else:
                    error = "Email is not correct.Try again!"
                    return render(request,"register.html",{"emailError": error})
        else:
            message = "Passwords don't match. Try again!"
            return render(request,"register.html",{"dontMatch":message})
        
def registration_done(request):
    return render(request, "registration_done.html")
        
def login_user(request):
    if request.method == "GET":
        return render(request, "login_user.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        username_exists = User.objects.filter(username=username).exists()
        if not username_exists:
            message = "This username does not exist. Try again!"
            return render(request, "login_user.html", {"noUser":message})
        else:
            userIsActive = User.objects.filter(username=username, is_active=True).exists()
            if not userIsActive:
                message = "This user is inactive. Please activate account and try again!"
                return render(request, "login_user.html", {"inactiveUser":message})
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("forumapp:home")
                else:
                    message = "Wrong password! Try again!"
                    return render(request, "login_user.html", {"wrongPass":message})

def logout_user(request):
    logout(request)
    return redirect("forumapp:home")
