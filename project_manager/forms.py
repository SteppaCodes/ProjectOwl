from django.forms import ModelForm
from . models import *

class MileStoneForm(ModelForm):
    class Meta:
        model = MileStone
        fields = "__all__"
        exclude = ['created_by', 'status','complete', 'project', 'value']

class PersonalProjectForm(ModelForm):
    class Meta:
        model = Project
        fields =   ['name','description','deadline', 'priority_level']
       
class CompanyProjectForm(ModelForm):

    class Meta:
        model = Project
        fields =   ['name','description','deadline', 'teams', 'priority_level']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields =['name', 'workers']

class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment
        fields =['name', 'file']

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['name','note']