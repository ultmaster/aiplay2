import os
import time

from django.contrib.auth.models import User
from django.test import TestCase

from program.models import Code, RunningReport
from judge.views import JudgeModule, create_solution
from program.views import create_code_object
from scene.views import ChallengeJudgeModule


class DemoTest(TestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(email="something@user.com", username="myusername")
        self.user.set_password("password")
        self.user.save()

    def test_2048(self):
        judge = create_code_object(open("demo/2048/judge.cpp", "r").read(), "cpp")
        solution = create_solution(open("demo/2048/random1.cpp", "r").read(), "cpp", self.user, "game")
        JudgeModule.judge_game(solution, judge, 2)
        print(solution.judge_report.raw_output)

    def test_2048_2(self):
        judge = create_code_object(open("demo/2048/judge.cpp", "r").read(), "cpp")
        solution = create_solution(open("demo/2048/random2.cpp", "r").read(), "cpp", self.user, "game")
        JudgeModule.judge_game(solution, judge, 2)
        print(solution.judge_report.raw_output)
        print(solution.user_report.return_code)
        print(solution.user_report.return_code)

    def test_gobang(self):
        judge = create_code_object(open("demo/gobang/judge.cpp", "r").read(), "cpp")
        solution1 = create_solution(open("demo/gobang/player1.cpp", "r").read(), "cpp", self.user, "combat")
        solution2 = create_solution(open("demo/gobang/player1.cpp", "r").read(), "cpp", self.user, "combat")
        a, b, j = ChallengeJudgeModule.judgea_combat(solution1, solution2, judge, 1)
        print(a.return_code, a.raw_output)
        print(b.return_code, b.raw_output)
        print(j.return_code, j.raw_output)
