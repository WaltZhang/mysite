from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name


class Dataset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)
    creation_date = models.DateTimeField('date created')

    def __str__(self):
        return self.name
