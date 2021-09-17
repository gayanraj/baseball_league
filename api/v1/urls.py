from django.urls import path, include
from rest_framework import routers

from api.v1.coach.views import CoachView
from api.v1.match.views import MatchView
from api.v1.match_player_stat.views import MatchPlayerStatView
from api.v1.player.views import PlayerView, PlayerStatView
from api.v1.season.views import SeasonView
from api.v1.team.views import TeamView, TeamStatView

router = routers.DefaultRouter()
router.register('coaches', CoachView)
router.register('players', PlayerView)
router.register('matches', MatchView)
router.register('seasons', SeasonView)
router.register('teams', TeamView)
router.register(r'match/players/stats', MatchPlayerStatView)

urlpatterns = [
    path(r'teams/stat/', TeamStatView.as_view(), name='team_stat'),
    path(r'teams/<int:team_id>/players/stat/', PlayerStatView.as_view(), name='team_players_stat'),
    path(r'', include(router.urls)),
]
