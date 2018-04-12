from django.contrib.auth.models import User
from django.db import models

from program.models import Code, RunningReport


class Solution(models.Model):
    code = models.ForeignKey(Code)
    create_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)


class GameSolution(Solution):
    score = models.PositiveIntegerField(default=0)
    user_report = models.ForeignKey(RunningReport, null=True, blank=True, related_name="user_report_set")
    judge_report = models.ForeignKey(RunningReport, null=True, blank=True, related_name="judge_report_set")

    def __str__(self):
        return "GameSolution " + str(self.code) + " - Score:" + str(self.score)


class CombatSolution(Solution):
    rating = models.IntegerField(default=0)
