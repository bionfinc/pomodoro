from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):

    def __str__(self):
        PK_string = str(self.pk)
        score_string = str(self.score)
        return_value = 'PK: ' + PK_string + ' Score: ' + score_string

        return return_value

    # Associate with the Django default user model
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    task_length = models.IntegerField(default=25)
    short_rest_length = models.IntegerField(default=5)
    long_rest_length = models.IntegerField(default=15)
    score = models.IntegerField(default=0)


# Signal information sourced from https://docs.djangoproject.com/en/3.0/topics/signals/
# Post-save signal info https://docs.djangoproject.com/en/3.0/ref/signals/#django.db.models.signals.post_save

# Create this model whenever a save is detected on a new django user model
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, raw, using, update_fields, **kwargs):
	# Check if new record was created
	if created:
		UserProfile.objects.create(account=instance)


# Update this model whenever a save is detected on the django user model
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, raw, using, update_fields, **kwargs):
	instance.userprofile.save()