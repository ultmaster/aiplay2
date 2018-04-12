import markdown
from django.db import models

from judge.models import Solution
from program.models import Code, RunningReport


class Scene(models.Model):
    TYPE_CHOICES = (
        ('game', 'Game'),
        ('combat', 'Combat')
    )

    title = models.CharField(max_length=192)
    statement = models.TextField(blank=True)
    time_limit = models.IntegerField(default=1000)
    judge = models.ForeignKey(Code, null=True, related_name="judge_set")
    html_analysis_code = models.ForeignKey(Code, null=True, related_name="analysis_set")
    scene_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    solutions = models.ManyToManyField(Solution, blank=True)

    def __str__(self):
        return self.get_scene_type_display() + ": " + self.title

    def get_statement_markdown(self):
        md = markdown.Markdown(
            extensions=['fenced_code',
                        'codehilite',
                        'tables',
                        ]
        )
        return md.convert(self.statement)


class Challenge(models.Model):
    code1 = models.ForeignKey(Solution, related_name="code1_set")
    code2 = models.ForeignKey(Solution, related_name="code2_set")
    create_time = models.DateTimeField(auto_now_add=True)
    accept_time = models.DateTimeField(blank=True, null=True)
    report0_judge = models.ForeignKey(RunningReport, null=True, related_name="report0_judge_set")
    report1 = models.ForeignKey(RunningReport, null=True, related_name="report1_set")
    report2 = models.ForeignKey(RunningReport, null=True, related_name="report2_set")
    score1 = models.IntegerField(default=0)
    score2 = models.IntegerField(default=0)
    belong_to = models.ForeignKey(Scene)
