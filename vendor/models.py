from django.db import models
from accounts.models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.utils import send_notification

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
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    if self.is_approved == True:
                        mail_subject = "Congratulations! Your restaurant is approved"
                        send_notification(mail_subject, mail_template, context)
                    else:
                        mail_subject = "We are sorry!, You are not eligible for publishing your food menu on our marketplace"
                        send_notification(mail_subject, mail_template, context)
                    
        return super(Vendor, self).save(*args, **kwargs)
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
