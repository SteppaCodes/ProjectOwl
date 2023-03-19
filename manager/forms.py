from django.forms import ModelForm
from . models import Team,Company

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company 
        fields= '__all__'
        exclude = ['owner']

class JoinCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_key']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name", "head"]

# class RoleForm(ModelForm):
#     class Meta:
#         model = Role
#         fields = ["title"]
