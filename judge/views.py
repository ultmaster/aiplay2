from django.shortcuts import render

from judge.models import GameSolution, CombatSolution
from program.models import Code, RunningReport
from program.views import run_two_programs, run_three_programs, compile_code, create_code_object


class JudgeModule(object):

    @staticmethod
    def fetch_score(report: RunningReport):
        try:
            last_line = report.raw_output.strip().split()[-1].strip()
            return tuple(map(int, tuple(last_line.split(","))))
        except:
            return (0, 0)

    @staticmethod
    def judge_game(solution: GameSolution, judge: Code, time_limit):
        solution.user_report, solution.judge_report = run_two_programs(solution.code, judge, time_limit)
        solution.score = JudgeModule.fetch_score(solution.judge_report)[0]
        solution.save()

    @staticmethod
    def judge_combat(solution_a: CombatSolution, solution_b: CombatSolution, judge: Code, time_limit):
        # report is not stored here
        a, b, j = run_three_programs(solution_a.code, solution_b.code, judge, time_limit)
        return a, b, j


def create_solution(code, lang, author, game_type):
    code = create_code_object(code, lang)
    if game_type == 'game':
        sol = GameSolution.objects.create(code=code, author=author)
    else:
        sol = CombatSolution.objects.create(code=code, author=author)
    return sol
