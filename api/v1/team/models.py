from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=200)
    logo = models.TextField(null=True)

    def __str__(self):
        return self.name
