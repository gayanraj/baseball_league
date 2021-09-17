from django.db import models

from api.v1.season.models import Season
from api.v1.team.models import Team


class Match(models.Model):
    MATCH_TYPE = (
        ("RS", "ROUND_OF_SIXTEEN"),
        ("QF", "QUARTER_FINAL"),
        ("SF", "SEMI_FINAL"),
        ("GF", "GRAND_FINAL")
    )

    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100, null=True)
    winner_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='winner_team')
    winner_team_score = models.IntegerField()
    lost_team = models.ForeignKey(Team, on_delete=models.RESTRICT, related_name='lost_team')
    lost_team_score = models.IntegerField()
    match_type = models.CharField(max_length=3, choices=MATCH_TYPE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + '_' + self.winner_team.name + '_vs_' + self.lost_team.name
