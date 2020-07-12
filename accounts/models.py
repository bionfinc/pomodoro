from django.db import models


# Create your models here.
class UserProfile(models.Model):

    def __str__(self):
        PK_string = str(self.pk)
        score_string = str(self.score)
        return_value = 'PK: ' + PK_string + ' Score: ' + score_string

        return return_value

    task_length = models.IntegerField()
    short_rest_length = models.IntegerField()
    long_rest_length = models.IntegerField()
    score = models.IntegerField()
