from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not instance.skip_signals:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if getattr(instance, 'skip_signals', False):
        return
    if not instance.skip_signals:
        profile, created = Profile.objects.get_or_create(user=instance)
        if created:
            profile.phone = instance.profile.phone  # Data dari register_view
            profile.address = instance.profile.address
            profile.save()

