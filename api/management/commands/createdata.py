import datetime
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from api.v1.coach.models import Coach
from api.v1.match.models import Match
from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.player.models import Player
from api.v1.season.models import Season
from api.v1.team.models import Team


class Command(BaseCommand):
    help = "python manage.py createdata"

    def handle(self, *args, **options):
        faker = Faker()
        with transaction.atomic():
            for _ in range(15):
                # create team
                team_name = faker.name()
                team = Team(name=team_name)
                team.save()

                # create coach
                coach_name = faker.name()
                coach = Coach(name=coach_name, team=team)
                coach.save()

                # create players
                for _ in range(10):
                    player_name = faker.name()
                    nic = str(random.randint(1, 10000000))
                    height = random.randint(165, 185)
                    player = Player(name=player_name, nic=nic, team=team, height=height)
                    player.save()

            # create season
            season = Season(name="Season X", start_date=datetime.date(2021, 1, 1),
                            end_date=datetime.date(2021, 12, 31))
            season.save()
            # create round of sixteen matches
            for i in range(1, 8):
                win_score = random.randint(1, 20)
                lost_score = random.randint(0, win_score)
                match = Match(date=datetime.date(2021, 9, 1), time=datetime.time(15, 30, 0), winner_team_id=i * 2 - 1,
                              lost_team_id=i * 2, winner_team_score=win_score, lost_team_score=lost_score,
                              match_type='RS', season=season)
                match.save()

                # create match player stats
                won_players = Player.objects.filter(team_id=i * 2 - 1)
                for player in won_players:
                    score = random.randint(0, win_score)
                    win_score -= score
                    stat = MatchPlayerStat(player=player, match=match, score=score)
                    stat.save()

                lost_players = Player.objects.filter(team_id=i * 2)
                for player in lost_players:
                    score = random.randint(0, lost_score)
                    lost_score -= score
                    stat = MatchPlayerStat(player=player, match=match, score=score)
                    stat.save()

        print('16 teams entered')
        print('16 coaches entered')
        print('160 players entered')
        print('8 matches in round of sixteen entered with player stats')
