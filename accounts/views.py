# from django.contrib.auth.models import
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth, messages

from contacts.models import Contact


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect('home')
    return redirect('home')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if not user:
            messages.error(request, "Incorrect credentials")
            return redirect('login')

        auth.login(request, user)
        messages.success(request, "Successfully logged in")
        return redirect('dashboard')

    return render(request, "accounts/login.html")


def register(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        User = get_user_model()

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, f"User with {email} email is already exists")
            return redirect('register')

        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password)
        auth.login(request, user)
        messages.success(request, "Account successfully created")
        user.save()
        return redirect('dashboard')

    return render(request, "accounts/register.html")


@login_required(login_url="login")
def dashboard(request):
    user_inquiries = Contact.objects.order_by("-created_at").filter(user_id=request.user.id)
    data = {
        "inquiries": user_inquiries
    }
    return render(request, "accounts/dashboard.html", data)
