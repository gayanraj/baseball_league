import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.v1.coach.models import Coach
from api.v1.match.models import Match
from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.player.models import Player
from api.v1.season.models import Season
from api.v1.team.models import Team


class TeamStatViewTest(APITestCase):
    def setUp(self):
        team_a = Team(name='Team A')
        team_a.save()
        team_b = Team(name='Team B')
        team_b.save()
        team_c = Team(name='Team C')
        team_c.save()
        season = Season(name='Season One', start_date=datetime.date(2021, 1, 1), end_date=datetime.date(2021, 12, 31))
        season.save()
        match = Match(date=datetime.date(2021, 9, 1), time=datetime.time(15, 30, 0), winner_team=team_a,
                      lost_team=team_b, winner_team_score=10, lost_team_score=5, match_type='RS',
                      season=season)
        match.save()
        match = Match(date=datetime.date(2021, 9, 2), time=datetime.time(15, 30, 0), winner_team=team_c,
                      lost_team=team_a, winner_team_score=10, lost_team_score=5, match_type='QF',
                      season=season)
        match.save()

    def test_get_team_stat(self):
        url = reverse('team_stat')
        response = self.client.get(url, {'tid': 1}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stat = response.data[0]['stat']
        total_score = stat.get('total_score')
        avg = stat.get('average_score')
        self.assertEqual(total_score, 15)
        self.assertEqual(avg, 7.5)


class PlayerStatViewTest(APITestCase):
    def setUp(self):
        team_a = Team(name='Team A')
        team_a.save()
        team_b = Team(name='Team B')
        team_b.save()
        team_c = Team(name='Team C')
        team_c.save()
        season = Season(name='Season One', start_date=datetime.date(2021, 1, 1), end_date=datetime.date(2021, 12, 31))
        season.save()
        match_one = Match(date=datetime.date(2021, 9, 1), time=datetime.time(15, 30, 0), winner_team=team_a,
                          lost_team=team_b, winner_team_score=10, lost_team_score=5, match_type='RS',
                          season=season)
        match_one.save()
        match_two = Match(date=datetime.date(2021, 9, 2), time=datetime.time(15, 30, 0), winner_team=team_c,
                          lost_team=team_a, winner_team_score=10, lost_team_score=5, match_type='QF',
                          season=season)
        match_two.save()
        player_a = Player(name='Player A', nic='123456780V', height=170, team=team_a)
        player_a.save()
        player_b = Player(name='Player B', nic='123456781V', height=170, team=team_a)
        player_b.save()
        player_c = Player(name='Player C', nic='123456782V', height=170, team=team_a)
        player_c.save()
        player_d = Player(name='Player D', nic='123456783V', height=170, team=team_a)
        player_d.save()
        player_e = Player(name='Player E', nic='123456784V', height=170, team=team_a)
        player_e.save()

        match_player_stat = MatchPlayerStat(match=match_one, player=player_a, score=5)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_one, player=player_b, score=4)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_one, player=player_c, score=3)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_one, player=player_d, score=2)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_one, player=player_e, score=2)
        match_player_stat.save()

        match_player_stat = MatchPlayerStat(match=match_two, player=player_a, score=6)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_two, player=player_b, score=3)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_two, player=player_c, score=2)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_two, player=player_d, score=1)
        match_player_stat.save()
        match_player_stat = MatchPlayerStat(match=match_two, player=player_e, score=0)
        match_player_stat.save()

        # player_a 5.5
        # player_a 3.5
        # player_a 2.5
        # player_a 1.5
        # player_a 1.0

        # 90 percentile is 5.5

    def test_get_team_players_stat(self):
        url = reverse('team_players_stat', kwargs={'team_id': 1})
        response = self.client.get(url, {'percentile': 90}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        stat = response.data[0]['stat']
        avg = stat.get('average_score')
        self.assertEqual(avg, 5.5)


class TeamTests(APITestCase):
    def setUp(self):
        team = Team(name='Team A')
        team.save()

    def test_create_team(self):
        """
        Ensure we can create a new Team object.
        """
        data = {'name': 'Team B', 'logo': None}
        response = self.client.post('/api/v1/teams/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)
        self.assertEqual(Team.objects.get(id=2).name, 'Team B')

    def test_get_team(self):
        """
        Ensure we can get Team objects.
        """
        response = self.client.get('/api/v1/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/api/v1/teams/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Team A')

    def test_update_team(self):
        """
        Ensure we can update a Team object.
        """
        data = {'name': 'Team C'}
        response = self.client.put('/api/v1/teams/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Team.objects.get().name, 'Team C')

    def test_delete_team(self):
        """
        Ensure we can delete a Team object.
        """
        response = self.client.delete('/api/v1/teams/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)


class CoachTests(APITestCase):
    def setUp(self):
        team = Team(name='Team A')
        team.save()
        coach = Coach(name='Coach A', team=team)
        coach.save()

    def test_create_coach(self):
        """
        Ensure we can create a new Coach object.
        """
        data = {'name': 'Coach B', 'team': 1}
        response = self.client.post('/api/v1/coaches/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Coach.objects.count(), 2)
        self.assertEqual(Coach.objects.get(id=2).name, 'Coach B')

    def test_get_coach(self):
        """
        Ensure we can get Coach objects.
        """
        response = self.client.get('/api/v1/coaches/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/api/v1/coaches/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Coach A')

    def test_update_coach(self):
        """
        Ensure we can update a Coach object.
        """
        data = {'name': 'Coach B', 'team': 1}
        response = self.client.put('/api/v1/coaches/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Coach.objects.get().name, 'Coach B')

    def test_delete_coach(self):
        """
        Ensure we can delete a Coach object.
        """
        response = self.client.delete('/api/v1/coaches/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Coach.objects.count(), 0)


class PlayerTests(APITestCase):
    def setUp(self):
        team = Team(name='Team A')
        team.save()
        player = Player(name='Player A', nic='123456780V', height=170, team=team)
        player.save()

    def test_create_player(self):
        """
        Ensure we can create a new Player object.
        """
        data = {'name': 'Player B', 'nic': '123456789V', 'height': 170, 'team': 1}
        response = self.client.post('/api/v1/players/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 2)
        self.assertEqual(Player.objects.get(id=2).name, 'Player B')

    def test_get_player(self):
        """
        Ensure we can get Player objects.
        """
        response = self.client.get('/api/v1/players/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/api/v1/players/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Player A')

    def test_update_player(self):
        """
        Ensure we can update a Player object.
        """
        data = {'name': 'Player B', 'nic': '123456789V', 'height': 170, 'team': 1}
        response = self.client.put('/api/v1/players/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Player.objects.get().name, 'Player B')

    def test_delete_player(self):
        """
        Ensure we can delete a Player object.
        """
        response = self.client.delete('/api/v1/players/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Player.objects.count(), 0)


class MatchTests(APITestCase):
    def setUp(self):
        team_a = Team(name='Team A')
        team_a.save()
        team_b = Team(name='Team B')
        team_b.save()
        season = Season(name='Season One', start_date=datetime.date(2021, 1, 1), end_date=datetime.date(2021, 12, 31))
        season.save()
        match = Match(date=datetime.date(2021, 9, 1), time=datetime.time(15, 30, 0), winner_team=team_a,
                      lost_team=team_b, winner_team_score=10, lost_team_score=5, match_type='GF',
                      season=season)
        match.save()

    def test_create_match(self):
        """
        Ensure we can create a new Match object.
        """
        data = {'date': '2021-09-01', 'time': '3:30:00', 'winner_team': 1, 'lost_team': 2, 'winner_team_score': 10,
                'lost_team_score': 5, 'match_type': 'GF',
                'season': 1}
        response = self.client.post('/api/v1/matches/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Match.objects.count(), 2)

    def test_get_match(self):
        """
        Ensure we can get Match objects.
        """
        response = self.client.get('/api/v1/matches/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/api/v1/matches/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_update_match(self):
        """
        Ensure we can update a Match object.
        """
        data = {'date': '2021-09-01', 'time': '3:30:00', 'winner_team': 1, 'lost_team': 2, 'winner_team_score': 8,
                'lost_team_score': 5, 'match_type': 'GF',
                'season': 1}
        response = self.client.put('/api/v1/matches/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Match.objects.get().winner_team_score, 8)

    def test_delete_match(self):
        """
        Ensure we can delete a Match object.
        """
        response = self.client.delete('/api/v1/matches/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Match.objects.count(), 0)


class MatchPlayerStatTests(APITestCase):
    def setUp(self):
        team_a = Team(name='Team A')
        team_a.save()
        player_a = Player(name='Player A', nic='123456789V', height=170, team=team_a)
        player_a.save()
        team_b = Team(name='Team B')
        team_b.save()
        player_b = Player(name='Player B', nic='123456780V', height=170, team=team_b)
        player_b.save()
        season = Season(name='Season One', start_date=datetime.date(2021, 1, 1), end_date=datetime.date(2021, 12, 31))
        season.save()
        match = Match(date=datetime.date(2021, 9, 1), time=datetime.time(15, 30, 0), winner_team=team_a,
                      lost_team=team_b, winner_team_score=10, lost_team_score=5, match_type='GF',
                      season=season)
        match.save()
        match_player_stat = MatchPlayerStat(match=match, player=player_a, score=5)
        match_player_stat.save()

    def test_create_match_player_stat(self):
        """
        Ensure we can create a new MatchPlayerStat object.
        """
        data = {'match': 1, 'player': 2, 'score': 2}
        response = self.client.post('/api/v1/match/players/stats/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchPlayerStat.objects.count(), 2)

    def test_get_match_player_stat(self):
        """
        Ensure we can get MatchPlayerStat objects.
        """
        response = self.client.get('/api/v1/match/players/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/api/v1/match/players/stats/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)

    def test_update_match_player_stat(self):
        """
        Ensure we can update a MatchPlayerStat object.
        """
        data = {'match': 1, 'player': 1, 'score': 3}
        response = self.client.put('/api/v1/match/players/stats/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MatchPlayerStat.objects.get().score, 3)

    def test_delete_match_player_stat(self):
        """
        Ensure we can delete a MatchPlayerStat object.
        """
        response = self.client.delete('/api/v1/match/players/stats/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MatchPlayerStat.objects.count(), 0)
