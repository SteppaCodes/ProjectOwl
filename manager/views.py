from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .models import *
from project_manager.models import *
from .forms import *
from users.forms import *
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from django.shortcuts import get_object_or_404


TODAY = datetime.date.today()

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
    user = request.user
    user.in_company = True
    user.save()
    logout(request)
    return redirect("login")

def joincompany(request):
    form = JoinCompanyForm()
    if request.method == "POST":
        company_id = request.POST.get("company_key")
        user = request.user

        form = JoinCompanyForm(request.POST)
        if form.is_valid():
            try:
                company = Company.objects.get(company_key=company_id)
                #Getting all the workers in a company
                members = company.worker_set.all()
                #querying the set to get the first worker with the same user as the present user
                member = members.filter(user=user).first()
                worker = user.worker
                #Checking if the user is not a member of a company
                if not member:
                    #checks if the user has a worker model and then sets user's company to teh company
                    if worker:
                        worker.company = company
                        worker.save()
                    #creates a new user object
                    else:
                       new = Worker.objects.create(user=user, company=company)
                       new.save()
                    return redirect("company-page", company.id)
                else:
                    messages.info(f"You are already a member of {company.name}")
                    form = JoinCompanyForm()
                    
            except Company.DoesNotExist:
                messages.error(request, "Invalid company id")
    else:
        form = JoinCompanyForm()

    context = {"form": form}
    return render(request, "manager/create-edit.html",context)

def switchaccount(request):
    User = get_user_model()
    user = request.user
    
    if user.in_company:
        user.in_company = False
        user.save()
        return redirect("user-dashboard", user.id)
    else:
        user.in_company = True
        user.save()
        # Check if the user is associated with any company
        if user.worker.company:
            user_company_key = user.worker.company.company_key
            request.session['company_key'] = user_company_key
            return redirect("company-page", user.worker.company.id)
        else:
            return redirect("join-company") 

def userdashboard(request, id):
    user = CostumUser.objects.get(id=id)
    profile = Profile.objects.get(user=user)

    if request.user.in_company:
        company_key = request.session.get('company_key')
        if company_key != None:
            company = Company.objects.get(company_key=company_key)
            #distinct() => Makes sure theres only one of each returned value
            projects = company.project_set.filter(teams__worker__user__username=user.username).distinct()

            context = {"user": user,
                        "profile": profile, 
                        "projects": projects, 
                        "count": projects.count()
                        }
        else:
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
    projects = company.project_set.all().order_by('-updated', '-created')
    teams = company.team_set.all()
    activities = company.activity_set.all()[:5]

    due_in = None
    for project in projects:
        deadline = project.deadline
        deadline = timezone.localtime(deadline)
        if deadline:
                due_in = int((deadline.date() - TODAY).days)
                project.due_in = due_in
                project.save()   
        else:
            project.due_in = None
            project.save()
   
    context = {'company':company,
                "workers":workers, 
                "projects":projects, 
                "teams": teams,
                "due_in":due_in,
                'activities':activities
                  }
    return render(request,'manager/company-page.html', context)

def create_update_team(request, team_id=None):
    team = None
    company = request.user.worker.company

    if team_id:
        team = get_object_or_404(Team, id=team_id)

    form = TeamForm(instance=team)
    if request.method == "POST":
        form = TeamForm(request.POST,instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.company = company
            team.save()

            activity = Activity.objects.create(
                user=request.user,
                team=team,
                message="created a new Team" 
                    if not team_id else "updated Team",
                company=request.user.worker.company,
                name=team.name
                )
            activity.save()

            return redirect('teams', company.id)

    context = {'form': form}
    return render(request,'manager/create-edit.html', context)

def teams(request,id):
    company = Company.objects.get(id=id)
    teams = company.team_set.all()
    activities = company.activity_set.all()[:5]

    context = {'teams': teams,
               'activities':activities
               }
    return render(request,'manager/teams.html', context)

def teamdashboard(request,id):
    team = Team.objects.get(id=id)
    members = team.worker_set.all()
    projects = Project.objects.filter(company=team.company)
    activities = team.company.activity_set.all()[:5]
    team_projects = []

    #getting projects the team is involved in
    for project in projects:
        if team in project.teams.all():
            team_projects.append(project)

    context = {
               "team":team,
               "members":members ,
               "projects":team_projects,
               "activities":activities
              }
    
    return render(request, "manager/team-dashboard.html", context)

def deleteteam(request,id):
    team = Team.objects.get(id=id)
    company = request.user.worker.company
    if request.method == "POST":
        team.delete()
        return redirect("teams", company.id)
    
    activity = Activity.objects.create(
            user=request.user,
            team=team,
            message= "Deleted team ",
            company=request.user.worker.company,
            name=team.name
                )
    activity.save()


    context = {"obj": team}
    return render(request,"manager/delete.html", context)