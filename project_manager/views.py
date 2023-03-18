from django.shortcuts import render,redirect
from .models import *
import os
from manager.models import *
from .forms import *
from .helpers import *
from django.http import HttpResponse,Http404
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404

#Work on Notes

def create_update_project(request, project_id=None):
    project = None

    if project_id:
        project = get_object_or_404(Project,id=project_id)
    
    if request.user.in_company:
        form = CompanyProjectForm(instance=project)
    else:
        form = PersonalProjectForm(instance=project)

    if request.method == "POST":
        if request.user.in_company:
            form = CompanyProjectForm(request.POST, instance=project)
        else:
            form = PersonalProjectForm(request.POST,instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            if request.user.in_company:
                #retrieving the company key from the session 
                key = request.session.get('company_key')
                #Getting the company data and setting the project.company
                #to the current company the user is looged in to
                company = Company.objects.get(company_key = key)
                project.company = company

                project.save()

                #getting the id of each department selected and adding it to the department row of the table
                for team_id in form.cleaned_data['teams']:
                    team = Team.objects.get(id=team_id.id)
                    project.teams.add(team)     
                
            else:
                project.is_personal = True
                project.created_by = request.user
                project.save()
                return redirect("user-dashboard", request.user.id)

            if request.user.in_company:
                company = request.user.worker.company

                activity = Activity.objects.create(
                    user=request.user,
                    project=project,
                    message="created a new Project" if not project_id else "updated Project",
                    company=company,
                    name=project.name
                )
                activity.save()
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
        if project.due_in < 7:
            project.priority_level = 'ASAP'
            project.save()
        else:
            project.priority_level = 'Normal'
            project.save()

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

    return render(request,'project_manager/project-page.html', context)

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

def create_update_milestone(request,id,milestone_id=None):
    project = Project.objects.get(id=id)
    milestone =None

    if milestone_id:
        milestone = get_object_or_404(MileStone,id=id)

    form = MileStoneForm(instance=milestone)
    if request.method == "POST":
        form = MileStoneForm(request.POST,instance=milestone)
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
                    message="created a new Milestone" if not milestone_id else "updated Milestone",
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
    return render(request,"project_manager/milestone-page.html", context)    

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

def create_update_task(request,id,task_id=None):
    milestone = MileStone.objects.get(id=id)
    task = None
    if task_id:
        task = get_object_or_404(Task, id=task_id)

    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST,instance=task)
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
                    message="created a new Task" 
                    if not task_id else "updated Task",
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

def files(request):
    company = request.user.worker.company
    attachments = company.attachment_set.all()
    print(attachments)
    context={
        'attachments':attachments
    }
    return render(request, 'project_manager/attachments.html', context)

def addfile(request,project_id=None,milestone_id=None, task_id=None,attachment_id=None):
    project = None
    milestone = None
    task = None
    attachment = None

    # Retrieve the project/milestone/task/attachment objects based on the parameters in the URL
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    if milestone_id:
        milestone = get_object_or_404(MileStone, id=milestone_id)
        project = milestone.project
    if task_id:
        task = get_object_or_404(Task, id=task_id)
        milestone = task.milestone
        project = milestone.project
    if attachment_id:
        attachment = get_object_or_404(Attachment, id=attachment_id)
        project = attachment.project
        milestone = attachment.milestone
        task = attachment.task

    form = AttachmentForm(instance=attachment)
    if request.method == 'POST':
        form = AttachmentForm(request.POST,request.FILES, instance=attachment)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.company = request.user.worker.company
            file.project = project
            file.milestone = milestone
            file.task = task
            file.save()
            return redirect('company-page', request.user.worker.company.id)

    context = {'form':form}
    return render(request, 'manager/create-edit.html', context)

def fileview(request, id):
    file = get_object_or_404(Attachment, id=id)
    file_path = file.file.path
    file_name, file_extension = os.path.splitext(file_path)

    #Not the best solution but the best i could figure out
    content_type = ''
    if file_extension == '.pdf':
        content_type = 'application/pdf'
    elif file_extension == '.jpg' or file_extension == '.jpeg':
        content_type = 'image/jpeg'
    elif file_extension == '.png':
        content_type = 'image/png'
    else:
        content_type = 'application/octet-stream'

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    return response

def deletefile(request,id):
    file = Attachment.objects.get(id=id)
    company = request.user.worker.company
    if request.method == "POST":
        file.delete()
        return redirect("company-page", company.id)

    context = {"obj": file}
    return render(request,"manager/delete.html", context)