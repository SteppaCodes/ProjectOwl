from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile,CostumUser


@receiver(post_save,sender=CostumUser)
def Profilesignal(sender, instance, created, **Kwargs):
    if created:
        Profile.objects.create(user=instance)