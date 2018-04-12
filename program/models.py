from django.db import models
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from sandbox.lang import SUPPORTED_LANG
import traceback


def transform_code_to_html(code, lang):
    return highlight(code, get_lexer_by_name(lang), HtmlFormatter())


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
        return str(self.pk) + ": " + self.code[:30] + "..."

    def code_html(self):
        return transform_code_to_html(self.code, self.language)


class RunningReport(models.Model):
    code = models.ForeignKey(Code)
    raw_output = models.TextField(blank=True)
    time_consumption = models.FloatField(default=0)
    return_code = models.IntegerField(default=0)
    finish_time = models.DateTimeField(blank=True, null=True)  # if this is null, this is not finished
