from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    phone_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=220, blank=True)
    location = models.PointField()
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
