from django.contrib import admin
from .models import Team, Worker, Company
from users.models import CostumUser

class TeamModelAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context,*args, **kwargs):
        key = request.session.get("company_key")
        company = Company.objects.get(company_key=key)
        
        context['adminform'].form.fields['head'].queryset  = Worker.objects.filter(company= company)
        return super().render_change_form(request, context, *args, **kwargs)



admin.site.register(Team, TeamModelAdmin)
admin.site.register(Worker)
admin.site.register(Company)
