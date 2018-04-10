import os
import time

from django.contrib.auth.models import User
from django.test import TestCase

from program.models import Code, RunningReport
from judge.views import JudgeModule, create_solution
from program.views import create_code_object


class DemoTest(TestCase):
    def test_2048(self):
        tmp_user = User.objects.create(email="something@user.com", username="myusername")
        tmp_user.set_password("password")
        tmp_user.save()
        judge = create_code_object(open("demo/2048/judge.cpp", "r").read(), "cpp")
        solution = create_solution(open("demo/2048/random1.cpp", "r").read(), "cpp", tmp_user, "game")
        JudgeModule.judge_game(solution, judge, 2)
        # print
