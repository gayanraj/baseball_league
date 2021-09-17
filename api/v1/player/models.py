from django.db import models

from api.v1.team.models import Team


class Player(models.Model):
    HEIGHT_UNIT = (
        ("cm", "CENTIMETERS"),
        ("m", "METERS"),
        ("in", "INCHES")
    )

    name = models.CharField(max_length=200)
    nic = models.CharField(max_length=20, unique=True)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    height_unit = models.CharField(max_length=2, choices=HEIGHT_UNIT, default='cm')
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name
