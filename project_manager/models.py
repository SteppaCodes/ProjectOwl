from django.db import models
from manager.models import *
from users.models import CostumUser
from datetime import timedelta


class Info(models.Model):

    STATUS = (
        ("In Progress", "In Progress"),
        ("In Queue", 'In Queue'),
        ("Paused", "Paused"),
        ("Completed", "Completed")
    )

    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    created_by = models.ForeignKey(CostumUser, on_delete=models.CASCADE, default='', null=True,blank=True)
    complete = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, default='In Queue',max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Project(Info):

    PRIORITY =(
        ('Normal', 'Normal'),
        ('ASAP','ASAP')
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, default = None, null=True, blank=True)
    progress = models.IntegerField(default=0, null=True, blank=True)
    priority_level = models.CharField(max_length=100, choices=PRIORITY, default='Normal')
    teams = models.ManyToManyField(Team, null=True, blank=True)
    deadline = models.DateTimeField(null = True, blank =True)
    is_personal = models.BooleanField(default=False, blank=True, null=True)
    due_in = models.IntegerField(null = True, blank=True, default=None)
    updated_by = models.ForeignKey(CostumUser, related_name="up_dated", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class MileStone(Info):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    value = models.IntegerField(default=0, null=True,blank=True)
    updated_by = models.ForeignKey(CostumUser, related_name="updated", on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-updated']
        verbose_name = "Milestone"
        verbose_name_plural = "Milestones"

    def __str__(self):
        return self.name
    

class Task(Info):
    milestone = models.ForeignKey(MileStone,on_delete=models.SET_NULL, null=True,blank=True)
    workers = models.ManyToManyField(Worker)
    start_time = models.DateTimeField(null=True, blank=True)
    pause_time = models.DurationField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))

    def __str__(self):
        return self.name


class Data(models.Model):
    name = models.CharField(max_length=200, default =None, null=True,blank=True)
    user = models.ForeignKey(CostumUser, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    milestone = models.ForeignKey(MileStone, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True,blank=True,default=None)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company,null=True,blank=True, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Activity(Data):
    message = models.CharField(max_length=2000, default= "New Activity")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.message
    

class Attachment(Data):
    STATUS = (
        ("Awaiting Review", "Awaiting Review"),
        ("In Review", 'In view'),
        ("Approved", "Approved"),
    )

    file = models.FileField(upload_to='files')
    status = models.CharField(choices=STATUS, default='Awaiting Review',max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated']
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"

class Note(models.Model):
    name = models.CharField(max_length=200)
    note = models.TextField()
    author = models.ForeignKey(CostumUser, on_delete=models.CASCADE,null=True,blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name