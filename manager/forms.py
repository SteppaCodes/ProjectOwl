from django.forms import ModelForm
from . models import Team,Project,MileStone, Company

class CreateCompanyForm(ModelForm):
    class Meta:
        model = Company 
        fields= '__all__'
        exclude = ['owner']

class MileStoneForm(ModelForm):
    class Meta:
        model = MileStone
        fields = "__all__"
        exclude = ['created_by', 'status','complete', 'project', 'value']

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["name", "head", "workers"]

# class RoleForm(ModelForm):
#     class Meta:
#         model = Role
#         fields = ["title"]

class PersonalProjectForm(ModelForm):
    class Meta:
        model = Project
        fields =   ['name','description','deadline']
       

class CompanyProjectForm(ModelForm):

    class Meta:
        model = Project
        fields =   ['name','description','deadline', 'teams',]
        
class JoinCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_key']