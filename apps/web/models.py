from django.core.exceptions import ValidationError
from django.db import models
from apps.users import models as user_models


class Patients(models.Model):
    class Meta:
        managed = True

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255)
    therapist = models.ForeignKey(user_models.CustomUser, on_delete=models.CASCADE, default=None)
    ts = models.DateTimeField(auto_now_add=True)
