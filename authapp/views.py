from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import SingUpForm, LoginForm


def signup(request):
    context = dict()
    form = SingUpForm()
    context['form'] = form

    if request.method == 'POST':
        form = SingUpForm(request.POST)
        context['form'] = form

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(username=username)
                if user is not None:
                    return render(request, 'authapp/signup.html', context)
            except:
                pass

            try:
                user = User.objects.get(email=email)
                if user is not None:
                    form.errors['email'] = 'A user with that email already exists.'
                    return render(request, 'authapp/signup.html', context)
            except:
                pass

        else:
            return render(request, 'authapp/signup.html', context)

        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.info(request, 'Registration successful')
        return redirect('authapp:login')
    else:
        context['form'] = SingUpForm()

    return render(request, 'authapp/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = dict()
    form = LoginForm()
    context['form'] = form

    if request.method == 'POST':
        form = LoginForm(request.POST)
        context['form'] = form

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = auth.authenticate(
                request, username=username_or_email, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('index')

            else:
                print('form')
                messages.error(request, 'Invalid credentials.')
                return render(request, 'authapp/login.html', context)

        else:
            print('hello')
            return render(request, 'authapp/login.html', context)

    else:
        context['form'] = LoginForm()

    return render(request, 'authapp/login.html', context)


@login_required(login_url='authapp:login')
def logout(request):
    auth.logout(request)
    return redirect('authapp:login')
