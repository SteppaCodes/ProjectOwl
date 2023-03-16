from django.shortcuts import render,redirect
from .models import *
from manager.models import *
from .forms import *
from .helpers import *
from django.http import HttpResponse
from django.utils import timezone


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

            if request.user.in_company:
                company = request.user.worker.company

                activity = Activity.objects.create(
                    user=request.user,
                    milestone=milestone,
                    message="created a new milestone",
                    company=company,
                    name=milestone.name
                )
                activity.save()

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

            activity = Activity.objects.create(
                    user=request.user,
                    milestone=milestone,
                    message= "updated milestone -> ",
                    company=request.user.worker.company,
                    name=milestone.name
                )
            activity.save()

            return redirect("project-page", milestone.project.id)

    context = {"form":form}
    return render(request,"manager/create-edit.html", context) 

def deletemilestone(request,id):
    milestone = MileStone.objects.get(id=id)
    company = request.user.worker.company
    
    if request.method == "POST":
        milestone.delete()

        activity = Activity.objects.create(
                    user=request.user,
                    milestone=milestone,
                    message="Deleted milestone",
                    company=company,
                    name=milestone.name
                )
        activity.save()

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

        activity = Activity.objects.create(
                    user=request.user,
                    task=task,
                    message= "Completed task",
                    name=task.name
                )
        activity.save()

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
                name= task.name,
                )
        activity.save()
    if request.method == "POST":
        task.delete()
        return redirect("milestone-page", task.milestone.id)

    context = {"obj": task}
    return render(request,"manager/delete.html", context)


