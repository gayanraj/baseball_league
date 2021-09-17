from django.db.models import Avg

from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.player.models import Player


class PlayerUtil:

    @staticmethod
    def filter_from_percentile(player_queryset, percentile):
        # get all team player average values
        pl_avg_list = []
        avg_scores = []
        for player in player_queryset:
            avg_score = MatchPlayerStat.objects.filter(player=player).aggregate(Avg('score')).get('score__avg')
            if not avg_score:
                avg_score = 0
            pl_avg = {
                'id': player.id,
                'avg': avg_score
            }
            pl_avg_list.append(pl_avg)
            avg_scores.append(avg_score)

        # sort lowest to highest
        avg_scores.sort()

        # calculate 90th percentile value
        index = round(percentile * len(avg_scores) / 100)
        percentile_threshold = avg_scores[index - 1]

        # filter players according to percentile threshold value
        eligible_players = []
        for pl_avg in pl_avg_list:
            score = pl_avg.get('avg')
            if score > percentile_threshold:
                player_id = pl_avg.get('id')
                eligible_players.append(player_id)

        eligible_quertset = Player.objects.filter(id__in=eligible_players)
        return eligible_quertset
