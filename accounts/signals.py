from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)    
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print("created")
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            print("created 11")
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            print("created 22")
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, "this use is being saved")
#post_save.connect(post_save_create_profile_receiver, sender=User)