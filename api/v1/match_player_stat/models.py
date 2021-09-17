from django.db import models

from api.v1.match.models import Match
from api.v1.player.models import Player


class MatchPlayerStat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)
    score = models.IntegerField(null=True)

    class Meta:
        unique_together = ['match', 'player']

    def __str__(self):
        return self.match.__str__() + '_' + self.player.name
