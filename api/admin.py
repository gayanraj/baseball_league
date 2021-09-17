from django.contrib import admin

from api.v1.coach.models import Coach
from api.v1.match.models import Match
from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.player.models import Player
from api.v1.season.models import Season
from api.v1.team.models import Team

admin.site.register(Team)
admin.site.register(Coach)
admin.site.register(Player)
admin.site.register(Season)
admin.site.register(Match)
admin.site.register(MatchPlayerStat)
