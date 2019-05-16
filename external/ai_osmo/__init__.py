from external._base import BasePairMatch
from functools import lru_cache
from os import path
if __name__ != '__mp_main__':  # 由参赛子进程中隔离django库
    from django.conf import settings

from . import osmo_api


class OsmoMatch(BasePairMatch):
    template_dir = 'renderer/osmo.html'

    class Meta(BasePairMatch.Meta):
        required_classes = [('Player', ['strategy'])]

    @classmethod
    def pre_run(cls, d_local, d_global):
        '''
        局间继承参数
        '''
        # 覆盖默认参数
        osmo_api.apply_params(d_local['params'])

        return [{}, {}]

    @classmethod
    def swap_fields(cls, d_local, d_global):
        '''
        交换场地
        '''
        cls.init_params = cls.init_params[::-1]

    @classmethod
    def run_once(cls, d_local, d_global):
        '''
        运行一局比赛
        并返回比赛记录对象
        '''
        return osmo_api.one_race(d_local['players'], cls.init_params,
                                 d_local['names'])

    @classmethod
    def output_queue(cls, world):
        '''
        读取比赛记录
        返回比赛结果元组
        '''
        res = world.result
        return (res['winner'], )

    @classmethod
    def save_log(cls, round_id, world, d_local, d_global):
        '''
        保存比赛记录
        '''
        match_dir = d_local['match_dir']
        log_name = path.join(match_dir, 'logs/%02d.zlog' % round_id)
        osmo_api.save_log(world, log_name)

    @classmethod
    @lru_cache()
    def load_record(cls, match_dir, rec_id):
        log_name = path.join(match_dir, 'logs/%02d.zlog' % rec_id)
        return osmo_api.load_log(log_name)

    @staticmethod
    def summary_records(records):
        '''
        统计比赛记录
        '''
        result_stat = {0: 0, 1: 0, None: 0}
        for rec in records:
            if rec == None:
                continue
            winner = rec['winner']
            if isinstance(winner, int) and rec["players"][0] == 'code2':
                winner = 1 - winner
            result_stat[winner] += 1
        return {
            'stat': result_stat,
        }


# 比赛记录显示模板
if __name__ != '__mp_main__':  # 由参赛子进程中隔离django库
    from external.tag_loader import RecordMeta

    class OsmoRecord(metaclass=RecordMeta(3)):
        def r_holder(_, match, record):
            if record['players'][0] == 'code1':
                return match.code1.name
            return match.code2.name

        def r_length(_, match, record):
            return len(record['data'])

        def r_winner(_, match, record):
            holder_win = record['winner']
            if holder_win == None:
                return '平手'

            code2_hold = (record['players'][0] == 'code2')
            code2_win = (code2_hold == holder_win)
            return '%s (%s, %s)' % (
                match.code2.name if code2_win else match.code1.name,
                ('发起方', '接收方')[code2_win],
                ('后手', '先手')[holder_win],
            )

        def r_win_desc(_, match, record):
            return '会有的'

        def r_desc_plus(_, match, record):
            return '会有的'
