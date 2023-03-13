from django.contrib import admin
from .models import CostumUser, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CostumUserCreationForm

# Register your models here.

class CostumUserAdmin(UserAdmin):
   model = CostumUser
   add_form = CostumUserCreationForm
   fieldsets = (
      *UserAdmin.fieldsets,(
      #sets the header text
      'Account Type', {
      "fields":(
      
        "in_company",

            )
        }
      )
   )


admin.site.register(CostumUser, CostumUserAdmin)
admin.site.register(Profile)
