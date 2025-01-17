from external._base import BasePairMatch
from external.factory import FactoryDeco
from external.helpers_core import stringfy_error
from .wrap import Game, register_player
import random, time


# 比赛进程
@FactoryDeco(6)
class TetrisMatch(BasePairMatch):
    class Meta(BasePairMatch.Meta):
        required_classes = [('Player', ['output'])]

    def get_timeout(self):
        '''获取超时限制'''
        return self.params['rounds'] * 30

    @classmethod
    def pre_run(cls, d_local, d_global):
        for module, name in zip(d_local['players'], d_local['names']):
            register_player(name, module)

    @classmethod
    def run_once(cls, d_local, d_global):
        # 每两轮更换固定种子
        if d_local['who_first'] != "4" or d_local['rid'] % 2 == 0:
            cls.last_seed = int(time.time() * 1000)
        random.seed(getattr(cls, 'last_seed'))

        play = Game(*d_local['names'], 10)
        while play.state == "gaming":
            play.turn()
        play.end()

        # 写入报错
        play.reviewData.gameData['errors'] = list(
            map(stringfy_error, play.errors))

        return play.reviewData.gameData

    @classmethod
    def _trans_winner(cls, record):
        ''' winner转换至平台设定 '''
        return record["winner"] - 1 if record["winner"] > 0 else None

    @classmethod
    def output_queue(cls, record):
        return (cls._trans_winner(record), )

    @classmethod
    def runner_fail_log(cls, winner, e, d_local, d_global):
        winner = winner + 1 if isinstance(winner, int) else -1
        names = d_local['names']
        log = {
            "player1": names[0],
            "player2": names[1],
            "winner": winner,
            "reason": stringfy_error(e),
            "tag": None,
            "matchData": {}
        }
        return log

    @classmethod
    def get_winner(cls, record):
        ''' 判断胜者 '''
        winner = cls._trans_winner(record)
        if winner != None and record['player1'] == 'code2':
            winner = 1 - winner
        return winner

    @classmethod
    def analyze_tags(cls, record):
        return record["tag"]