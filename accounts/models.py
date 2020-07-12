from django.db import models


# Create your models here.
class UserProfile(models.Model):

    def __str__(self):
        return_value = 'PK: ' + str(self.pk) + ' Score: ' + self.score

        return return_value

    task_length = models.IntegerField()
    short_rest_length = models.IntegerField()
    long_rest_length = models.IntegerField()
    score = models.IntegerField()
