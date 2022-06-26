from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .models import Problem, Submission

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username1 = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Incorrect username or password")
    return render(request, 'login.html')

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def homePage(request):
    problems = Problem.objects.all()
    context = {'problems':problems, 'username':request.user.username}
    return render(request, 'problems-page.html', context)

@login_required(login_url='login')
def problemPage(request, pk):
    problem = Problem.objects.get(id=pk)
    context = {'problem':problem, 'username':request.user.username}
    return render(request, 'problem-desc-page.html', context)

@login_required(login_url='login')
def submissionPage(request, pk):
    if request.method == "POST":
        username = request.user
        problem_id = request.POST.get('problem_id')
        print(username, problem_id)
        return HttpResponse("submitted")
    else:
        problem = Problem.objects.get(id=pk)
        context = {'problem':problem, 'username':request.user.username}
        return render(request, 'submissions-page.html', context)