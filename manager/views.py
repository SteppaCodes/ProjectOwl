from django.shortcuts import render,redirect
from .helpers import TODAY
from .models import *
from .forms import *
from users.forms import *
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def signup(request):
    page = "Signup"
    form = CostumUserCreationForm()
    if request.method == "POST":
        form = CostumUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("user-dashboard", user.id)
        else:
            form = CostumUserCreationForm()

    context = {"page":page,
                "form": form}
    return render(request, 'manager/login-register.html', context)

def loginUser(request):
    page = "Login"

    if request.method == "POST":
        company_id = request.POST.get("company_id")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.in_company:
                try:
                    if company_id:
                        company = Company.objects.get(company_key=company_id)
                        #filter through the worker and get
                        if company.worker_set.filter(user=user).exists():
                            request.session['company_key'] = company_id
                            login(request, user)
                            print(user.in_company)
                            return redirect("company-page", company.id)
                        else:
                            messages.error(request, "User is not associated with this company")
                    #this function is for users who have a
                    #  company account but wants to login to 
                    # their personal account so it does that 
                    # if the company id field is left blank
                    else:
                        user.in_company = False
                        user.save()
                        login(request,user)
                        print(user.in_company)
                        return redirect("user-dashboard", user.id)
                except Company.DoesNotExist:
                    messages.error(request, "Company does not exist")
            else:
                login(request, user)
                print(user.in_company)
                return redirect("user-dashboard", user.id)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'manager/login-register.html', {"page": "Login"})

def logoutuser(request):
    logout(request)
    return redirect("login")


def userdashboard(request, id):
    user = CostumUser.objects.get(id=id)
    profile = Profile.objects.get(user=user)

    if request.user.in_company:
        company_key = request.session.get('company_key')
        if company_key != None:
            company = Company.objects.get(company_key=company_key)
            #distinct() => Makes sure theres only one of each returned value
            projects = company.project_set.filter(teams__workers__user__username=user.username).distinct()

            context = {"user": user,
                        "profile": profile, 
                        "projects": projects, 
                        "count": projects.count()
                        }
        else:
            #messages.error("You do not have a company account")
            return redirect("login")
    else:
        user = request.user
        projects = user.project_set.filter(is_personal=True)
        count = projects.count()
        for project in projects:
            deadline = project.deadline
            if project.deadline:
                project.due_in = deadline.date() - TODAY
                project.due_in = project.due_in.days
                project.save()

        context = {"profile":profile,
                    'projects':projects, 
                    'count':count
                    }
    
    return render(request,'manager/user-dashboard.html', context)

def companypage(request,id):
    company = Company.objects.get(id=id)
    workers = company.worker_set.all()
    projects = company.project_set.all()
    teams = company.team_set.all()

    due_in = 0
    for project in projects:
        deadline = project.deadline
        deadline = timezone.localtime(deadline)
        if deadline:
                due_in = int((deadline.date() - TODAY).days)
                project.due_in = due_in
                project.save()   
   
    context = {'company':company,
                "workers":workers, 
                "projects":projects, 
                "teams": teams,
                "due_in":due_in
                  }
    return render(request,'manager/company-page.html', context)

def ProjectPage(request, id):
    project = Project.objects.get(id=id)
    milestones = project.milestone_set.all()
    deadline = project.deadline
    deadline = timezone.localtime(deadline)
    count = milestones.count()

    if deadline:
        due_in = int((deadline.date() - TODAY).days)
        project.due_in = due_in

    if request.user.in_company:
        teams = project.teams.all()
        workers = []
        project.progress = 0

        #Getting Each worker in departments that are working on the project
        for team in teams:
            for worker in team.workers.all():
                if worker not in workers:
                    workers.append(worker)

        #Creating a value for each milestone
        #this will affect the project progress - if all milestones are complete
        #the project progress = 100% 
        if count > 0:
            value = 100 / count
        #Assigning the value to each milestone
        for milestone in milestones:
            milestone.value = int(value)
            #Increasing the value of project progress if the milestone is completed
            if milestone.status == "Completed":
                project.progress += milestone.value
                project.save()

        context = {"project":project,
                   'milestones':milestones,
                    'count':count,
                    'teams':teams, 
                    "workers":workers,
                    'due_in':due_in }
    else:
        if count > 0:
            value = 100 / count

        for milestone in milestones:
            milestone.value = int(value)
            #Increasing the value of project progress if the milestone is completed
            if milestone.status == "Completed":
                project.progress += milestone.value
                project.save()

        context =  {"milestones": milestones,
                     "project": project,
                     'due_in':due_in,}   

    return render(request,'manager/project-page.html', context)

