from django.db import models

from api.v1.team.models import Team


class Coach(models.Model):
    name = models.CharField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name
