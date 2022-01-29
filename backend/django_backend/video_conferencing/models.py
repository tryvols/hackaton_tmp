import random

from django.db import models
from authentication.models import User


# Create your models here.
class Conference(models.Model):
    ID = models.AutoField(primary_key=True)
    url = models.CharField(max_length=13)
    is_open = models.BooleanField(default=True)


class Members(models.Model):
    ID = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conference_id = models.ForeignKey(Conference, on_delete=models.CASCADE)
    is_admin = models.BooleanField()
