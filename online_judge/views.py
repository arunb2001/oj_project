import os, filecmp
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .models import Problem, Submission
from django.contrib.auth.models import User

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
    submissions = Submission.objects.all().order_by("-timestamp")
    leaderboard = {}
    for user in User.objects.all():
        leaderboard[user.username] = Submission.objects.filter(userID=user.id).count()
    leaderboard = {key:leaderboard[key] for key in sorted(leaderboard, key=lambda v: v[1], reverse=True)}
    context = {'problems':problems, 'submissions':submissions, 'leaderboard':leaderboard, 'username':request.user.username}
    return render(request, 'problems-page.html', context)

@login_required(login_url='login')
def problemPage(request, pk):
    username = request.user
    user = User.objects.get(username=username)
    problem = Problem.objects.get(id=pk)
    submissions = Submission.objects.filter(problemID=problem.id, userID=user.id).order_by("-timestamp")
    context = {'problem':problem, 'username':request.user.username, 'submissions':submissions}
    return render(request, 'problem-desc-page.html', context)

@login_required(login_url='login')
def submissionPage(request, pk):
    if request.method == "POST":
        username = request.user
        problem_id = request.POST.get('problem_id')
        code = request.POST.get('code')

        problem = Problem.objects.get(id=problem_id)
        user = User.objects.get(username=username)
        submissionCount = Submission.objects.filter(problemID=problem.id, userID=user.id).count()
        submissionFilename = user.username+'_'+str(problem.id)+'_'+str(submissionCount+1)+'.txt'
        codeFile = os.path.join('submissions', submissionFilename)
        inFile = os.path.join('input_files', problem.inputFile)
        outFile = os.path.join('output_files', problem.outputFile)
        with open(codeFile, 'w') as file:
            file.write(code)
        with open('solution.cpp', 'w') as file:
            file.write(code)
        if os.path.exists('sol.exe'):
            os.system('del sol.exe')
        if os.system('g++ solution.cpp -o sol.exe & sol < '+ inFile +' > out.txt') != 0:
            verdict = 'Compilation Error'
        elif filecmp.cmp('out.txt', outFile, shallow=False):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
        submission = Submission(problemID=problem, userID=user, verdict=verdict, code=submissionFilename)
        submission.save()
        context = {'problem':problem, 'username':request.user.username, 'verdict':verdict}
        return render(request, 'verdict.html', context)
    else:
        return redirect('/problem/'+str(pk))

@login_required(login_url='login')
def codePage(request, code):
    with open(os.path.join('submissions', code), 'r') as file:
        content = file.read()
    return HttpResponse(content, content_type="text/plain")