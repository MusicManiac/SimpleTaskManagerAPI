from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Task(models.Model):
    STATUS_CHOICES = [ # task statuses
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    id = models.AutoField(primary_key=True) # auto-incremented id
    name = models.CharField(max_length=255) # short name, required
    description = models.TextField(blank=True, null=True) # description, optional and can be null in table
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new') # status
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # many-to-one relationship to User
    history = HistoricalRecords() # https://django-simple-history.readthedocs.io/en/latest/

    def __str__(self):
        return self.name