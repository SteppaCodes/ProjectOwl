from django.db import models
from users.models import CostumUser
from datetime import timedelta

# Create your models here.
class ProjectInfo(models.Model):

    STATUS = (
        ("In Progress", "In Progress"),
        ("In Queue", 'In Queue'),
        ("Paused", "Paused"),
        ("Completed", "Completed")
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, default='In Queue',max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Company(models.Model):
    name = models.CharField( max_length=200,verbose_name="Companies")
    owner = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    website = models.URLField(default='', max_length=2000, null=True, blank=True)
    description = models.TextField()
    company_key = models.CharField(max_length=200, default='0000')
    logo = models.ImageField( default='', upload_to="logos/",null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Team(models.Model):
    name = models.CharField(max_length=200,verbose_name="Teams")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    head = models.OneToOneField("Worker", default= "No Head" ,related_name="head",on_delete=models.SET_NULL, null=True, blank=True)
    workers = models.ManyToManyField("Worker")

    def __str__(self):
        return self.name
    

class Worker(models.Model):
    user = models.OneToOneField(CostumUser,on_delete=models.CASCADE,verbose_name="Workers")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,blank=True,default='Company Not Set')

    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"


class Project(ProjectInfo):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default = 'No company', null=True, blank=True)
    progress = models.IntegerField(default=0, null=True, blank=True)
    teams = models.ManyToManyField(Team, null=True, blank=True)
    deadline = models.DateTimeField(null = True, blank =True)
    is_personal = models.BooleanField(default=False, blank=True, null=True)
    due_in = models.IntegerField(null = True, blank=True)
    updated_by = models.ForeignKey(CostumUser, related_name="up_dated", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class MileStone(ProjectInfo):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, null=True,blank=True)
    updated_by = models.ForeignKey(CostumUser, related_name="updated", on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ['-updated']
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"

    def __str__(self):
        return self.name
    
class Task(models.Model):
    name = models.CharField(max_length=200, default='New Task',verbose_name = "Milestone")
    start_time = models.DateTimeField(null=True, blank=True)
    pause_time = models.DurationField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))
                                                        
                                                     
class Activity(models.Model):
    user = models.ForeignKey(CostumUser, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    milestone = models.ForeignKey(MileStone, on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=2000, default= "New Activity")
    company = models.ForeignKey(Company,null=True,blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.message