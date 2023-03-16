from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Project)
admin.site.register(MileStone)
admin.site.register(Attachment)
admin.site.register(Task)
admin.site.register(Activity)