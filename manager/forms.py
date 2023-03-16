from django.forms import ModelForm
from . models import Team,Company

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company 
        fields= '__all__'
        exclude = ['owner']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name", "head", "workers"]

# class RoleForm(ModelForm):
#     class Meta:
#         model = Role
#         fields = ["title"]
