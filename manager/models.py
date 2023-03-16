from django.db import models
from users.models import CostumUser


class Company(models.Model):
    name = models.CharField( max_length=200,verbose_name="Companies")
    owner = models.ForeignKey(CostumUser, on_delete=models.CASCADE)
    website = models.URLField(default='', max_length=2000, null=True, blank=True)
    description = models.TextField()
    company_key = models.CharField(max_length=200, default=None)
    logo = models.ImageField( default='', upload_to="logos/",null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def getlogo(self):
        try:
            url = self.logo.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.name
    

class Team(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    head = models.OneToOneField("Worker", default= None ,related_name="head",on_delete=models.SET_NULL, null=True, blank=True)
    workers = models.ManyToManyField("Worker")
    updated_by = models.ForeignKey(CostumUser, related_name="update_team", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.name
    

class Worker(models.Model):
    user = models.OneToOneField(CostumUser,on_delete=models.CASCADE,verbose_name="Workers")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True,blank=True,default=None)

    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        verbose_name = "Worker"
        verbose_name_plural = "Workers"

