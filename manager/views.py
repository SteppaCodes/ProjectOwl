from django.shortcuts import render
from .helpers import TODAY
from .models import *
from django.utils import timezone



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