from django.db import models

# Create your models here.

from django.db import models

class BeamInput(models.Model):
    length = models.FloatField()
    point_load = models.FloatField(null=True, blank=True)
    udl = models.FloatField(null=True, blank=True)  # Uniformly Distributed Load
    support_type = models.CharField(max_length=20, choices=[('Fixed', 'Fixed'), ('Simply Supported', 'Simply Supported')])
