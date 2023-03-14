from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Project,Worker, MileStone,Activity
from users.models import CostumUser


@receiver(post_save,sender= CostumUser)
def create_work_profile(sender,instance,**Kwargs):

    if instance.in_company:
        Worker.objects.get_or_create(user=instance)

@receiver(post_save,sender= Project)
def create_project_activity(sender,created,instance,**Kwargs):
    if created:
        if instance.created_by.in_company:
            activity = Activity.objects.create(
                user= instance.created_by,
                project= instance,
                message =  "created a new project ",
                company=instance.created_by.worker.company
            )
            print(activity.message)
    else:
        if instance.created_by.in_company:
            activity = Activity.objects.create(
                user= instance.updated_by,
                project= instance,
                message =  "Updated",
                company=instance.created_by.worker.company
            )
            print(activity.message)
