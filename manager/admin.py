from django.contrib import admin
from .models import Project, MileStone, Team, Worker, Company, Task,Activity
from users.models import CostumUser

# Register your models here.

# class TeamModelAdmin(admin.ModelAdmin):
#     def render_change_form(self, request, context,*args, **kwargs):
#         context['adminform'].form.fields['workers'].queryset  = CostumUser.objects.filter(in_company=True)
#         key = request.session.get("company_key")
#         company = Company.objects.get(company_key=key)
        
#         context['adminform'].form.fields['workers'].queryset  = Worker.objects.filter(company= company)
#         context['adminform'].form.fields['head'].queryset  = Worker.objects.filter(company= company)
#         return super().render_change_form(request, context, *args, **kwargs)


admin.site.register(Project)
admin.site.register(MileStone)
#admin.site.register(Department, DepartmentModelAdmin)
admin.site.register(Worker)
admin.site.register(Company)
admin.site.register(Task)
admin.site.register(Activity)