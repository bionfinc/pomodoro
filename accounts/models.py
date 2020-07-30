from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserProfile(models.Model):
    PLANT_STAGE_CHOICES = [
        (1, 'seed'),
        (2, 'plant_stage2'),
        (3, 'plant_stage3'),
        (4, 'plant_stage4'),
        (5, 'plant_stage5'),
        (6, 'plant_stage6'),
        (7, 'plant_stage7'),
    ]

    AWARD_CHOICES = [
        (0, 'empty_plate'),
        (1, 'tomato_basil_spaghetti'),
        (2, 'tomato_lasagna'),
        (3, 'tomato_pizza'),
        (4, 'tomato_sauce_penne'),
        (5, 'tomato_sauce_spaghetti'),
    ]

    def __str__(self):
        pk_string = str(self.pk)
        score_string = str(self.score)
        return_value = 'PK: ' + pk_string + ' Score: ' + score_string

        return return_value

    # Associate with the Django default user model
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    task_length = models.IntegerField(default=25)
    short_rest_length = models.IntegerField(default=5)
    long_rest_length = models.IntegerField(default=15)
    score = models.IntegerField(default=0)
    plant1_stage = models.IntegerField(choices=PLANT_STAGE_CHOICES, default=1)
    plant2_stage = models.IntegerField(choices=PLANT_STAGE_CHOICES, default=1)
    plant3_stage = models.IntegerField(choices=PLANT_STAGE_CHOICES, default=1)
    award_count = models.IntegerField(default=0)
    award1 = models.IntegerField(choices=AWARD_CHOICES, default=0)
    award2 = models.IntegerField(choices=AWARD_CHOICES, default=0)
    award3 = models.IntegerField(choices=AWARD_CHOICES, default=0)


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
