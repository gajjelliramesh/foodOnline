from django.db import models
from accounts.models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
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
