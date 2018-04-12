from django.db import models
from sandbox.lang import SUPPORTED_LANG
import traceback


class Code(models.Model):

    code = models.TextField()
    language = models.CharField(choices=SUPPORTED_LANG, max_length=12)
    workspace = models.CharField(max_length=192, blank=True)
    is_compiled = models.IntegerField(choices=(
        (0, 'Unknown'),
        (1, 'Success'),
        (2, 'Failed'),
    ), default=0)
    compiler_message = models.TextField(blank=True)

    def __str__(self):
        return str(self.pk) + ": " + self.code[:20] + "..."


class RunningReport(models.Model):
    code = models.ForeignKey(Code)
    raw_output = models.TextField(blank=True)
    time_consumption = models.FloatField(default=0)
    return_code = models.IntegerField(default=0)
    finish_time = models.DateTimeField(blank=True, null=True)  # if this is null, this is not finished
