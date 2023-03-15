from django.db.models.signals import pre_save, post_save,pre_delete
from django.dispatch import receiver
from .models import Project,Worker
from users.models import CostumUser
from datetime import datetime, timedelta


@receiver(post_save,sender= CostumUser)
def create_work_profile(sender,instance,**Kwargs):

    if instance.in_company:
        Worker.objects.get_or_create(user=instance)

