import random

from django.db import models
from authentication.models import User


def create_conf_code():
    chars = '1234567890qwertyuiopasdfghjklzxcvbnm'
    code = ''.join([random.choice(chars) for _ in range(0, random.randint(6, 12))])
    return code


# Create your models here.
class Conference(models.Model):
    ID = models.AutoField(primary_key=True)
    url = models.CharField(default=create_conf_code(),  max_length=13)
    is_open = models.BooleanField(default=True)


class Members(models.Model):
    ID = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    conference_id = models.ForeignKey(Conference, on_delete=models.CASCADE)
    is_admin = models.BooleanField()
