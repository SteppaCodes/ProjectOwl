from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from .helpers import TODAY
from .models import *
from .forms import *
from users.forms import *
from django.contrib.auth import get_user_model
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
            projects = company.project_set.filter(teams__workers__user__username=user.username).distinct()

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
    projects = company.project_set.all()
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

def createproject(request):

    if request.user.in_company:
        form = CompanyProjectForm()
    else:
        form = PersonalProjectForm()

    if request.method == "POST":
        if request.user.in_company:
            form = CompanyProjectForm(request.POST)
        else:
            form = PersonalProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            if request.user.in_company:
                #retrieving the company key from the session 
                key = request.session.get('company_key')
                #Getting the company data and setting the project.company to the current company the user is looged in to
                company = Company.objects.get(company_key = key)
                project.company = company
            else:
                project.is_personal = True
                project.created_by = request.user
                project.save()
                return redirect("user-dashboard", request.user.id)
            
            project.save()

            if request.user.in_company:
                company = request.user.worker.company

                activity = Activity.objects.create(
                    user=request.user,
                    project=project,
                    message="created a new project",
                    company=company,
                    name=project.name
                )
                activity.save()
            
            #getting the id of each department selected and adding it to the department row of the table
            for team_id in form.cleaned_data['teams']:
                team = Team.objects.get(id=team_id.id)
                project.teams.add(team)

            return redirect("company-page", company.id)
        
    context = {"form":form}
    return render(request,"manager/create-edit.html", context)

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

def updateproject(request, id):
    project = Project.objects.get(id=id)

    if request.user.in_company:
        form = CompanyProjectForm(instance=project)
    else:
        form = PersonalProjectForm(instance=project)
    company = project.company

    if request.method == "POST":
        if request.user.in_company:
            form = CompanyProjectForm(request.POST,instance=project)
        else:
            form = PersonalProjectForm(request.POST,instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            if request.user.in_company:
                project.company = company
                project.updated_by = request.user
                project.save()

                activity = Activity.objects.create(
                    user=request.user,
                    project=project,
                    message= f"updated project -> ",
                    company=company,
                    name=project.name
                )
                activity.save()

            # Clear existing teams
                project.teams.clear()

                for team_id in form.cleaned_data['teams']:
                    team = Team.objects.get(id=team_id.id)
                    project.teams.add(team)
            else:
                project.save()
            
            return redirect("project-page", project.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context) 

def deleteproject(request,id):
    project = Project.objects.get(id=id)
    if request.user.in_company:
            company = request.user.worker.company
            activity = Activity.objects.create(
                    user=request.user,
                    project=project,
                    message="deleted -",
                    company=company,
                    name= project.name
                )
            activity.save()
    if request.method == "POST":
        project.delete()
        if request.user.in_company:
            return redirect("company-page", project.company.id)
        else:
            return redirect("user-dashboard", request.user.id)
    
    context = {"obj":project}
    return render(request,"manager/delete.html", context)

def createmilestone(request, id):
    project = Project.objects.get(id=id)
    form = MileStoneForm()
    if request.method == "POST":
        form = MileStoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.created_by = request.user
            milestone.save()
            return redirect("project-page", project.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context)

def milestonepage(request, id):
    milestone = MileStone.objects.get(id=id)
    tasks = milestone.task_set.all()

    context = {"milestone": milestone , 'tasks':tasks}
    return render(request,"manager/milestone-page.html", context)    

def updatemilestone(request, id):
    milestone = MileStone.objects.get(id=id)
    form = MileStoneForm(instance=milestone)
    if request.method == "POST":
        form = MileStoneForm(request.POST, instance=milestone)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.save()
            return redirect("project-page", milestone.project.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context) 

def deletemilestone(request,id):
    milestone = MileStone.objects.get(id=id)
    
    if request.method == "POST":
        milestone.delete()
        return redirect("project-page", milestone.project.id)

    context = {"obj":milestone}
    return render(request,"manager/delete.html", context)

def createtask(request, id):
    milestone = MileStone.objects.get(id=id)
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.milestone = milestone
            task.created_by=request.user
            task.save()

            if request.user.in_company:
                company = request.user.worker.company

                activity = Activity.objects.create(
                    user=request.user,
                    task=task,
                    message="created a new task",
                    company=company,
                    name=task.name
                )
                activity.save()

            for worker_id in form.cleaned_data['workers']:
                worker = Worker.objects.get(id=worker_id.id)
                task.workers.add(worker)
            return redirect("milestone-page", milestone.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context)

def updatetask(request, id):
    task =Task.objects.get(id=id)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            activity = Activity.objects.create(
                    user=request.user,
                    task=task,
                    message= "updated task",
                    name=task.name
                )
            activity.save()

            task.workers.clear()

            for worker_id in form.cleaned_data['workers']:
                worker = Worker.objects.get(id=worker_id.id)
                task.workers.add(worker)

            return redirect("milestone-page", task.milestone.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context) 

def starttask(request, id):
    task = Task.objects.get(id=id)

    if request.method == "GET":
        NOW = timezone.now()
        #Set the start time of the milestone to the current time
        task.start_time = NOW
        task.status = "In Progress"
        task.save()
        return redirect('milestone-page', task.milestone.id)

def pausetask(request,id):
    task = Task.objects.get(id=id)
    
    if request.method == "GET":
        NOW = timezone.now()

        if task.time_spent is not None:
            if task.status != "Paused":
                task.time_spent += (NOW - task.start_time)
                task.start_time = None
                task.status = "Paused"
                task.save()
            else:
                return HttpResponse("milestone is not in progress")
        return redirect('milestone-page', task.milestone.id)

def completetask(request,id):
    task = Task.objects.get(id=id)
    
    if request.method == "GET":
        task.status = "Completed"
        task.complete = True
        task.save()
        return redirect('milestone-page', task.milestone.id)

def deletetask(request,id):
    task = Task.objects.get(id=id)
    if request.user.in_company:
        company = request.user.worker.company
        activity = Activity.objects.create(
                user=request.user,
                task=task,
                message="deleted task",
                company=company,
                name= task.name
                )
        activity.save()
    if request.method == "POST":
        task.delete()
        return redirect("milestone-page", task.milestone.id)

    context = {"obj": task}
    return render(request,"manager/delete.html", context)

def createteam(request):
    form = TeamForm()
    company = request.user.worker.company

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.company = company
            team.save()

            for worker_id in form.cleaned_data['workers']:
                worker = Worker.objects.get(id=worker_id.id)
                team.workers.add(worker)

            return redirect('teams', company.id)

    context = {'form': form}
    return render(request,'manager/create-edit.html', context)

def teams(request,id):
    company = Company.objects.get(id=id)
    teams = company.team_set.all()

    context = {'teams': teams}
    return render(request,'manager/teams.html', context)

def teamdashboard(request,id):
    team = Team.objects.get(id=id)
    members = team.workers.all()
    projects = Project.objects.filter(company=team.company)
    team_projects = []

    #getting projects the team is involved in
    for project in projects:
        if team in project.teams.all():
            team_projects.append(project)

    context = {
               "team":team,
               "members":members ,
               "projects":team_projects
              }
    
    return render(request, "manager/team-dashboard.html", context)

def updateteam(request, id):
    team = Team.objects.get(id=id)
    form = TeamForm(instance=team)


    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.updated_by = request.user
            team.save()

            team.workers.clear()

            for worker_id in form.cleaned_data['workers']:
                worker = Worker.objects.get(id=worker_id.id)
                team.workers.add(worker)

            return redirect('team-dashboard', team.id)

    context = {'form': form}
    return render(request,'manager/create-edit.html', context)

def deleteteam(request,id):
    team = Team.objects.get(id=id)
    company = request.user.worker.company
    if request.method == "POST":
        team.delete()
        return redirect("teams", company.id)

    context = {"obj": team}
    return render(request,"manager/delete.html", context)
