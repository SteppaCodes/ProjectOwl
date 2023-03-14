from django.shortcuts import render
from .helpers import TODAY
from .models import *
from django.utils import timezone



def home(request):
    return render(request,'manager/home.html')

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