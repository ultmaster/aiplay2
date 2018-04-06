import time
from django.test import TestCase

from program.models import Code, RunningReport
from .views import run_two_programs, compile_code

class ProgramTest(TestCase):
    def test_two_programs(self):
        c1 = Code.objects.create(code=open("program/testdata/int1.cpp").read(),
                                 language="cpp")
        c2 = Code.objects.create(code=open("program/testdata/int1res.cpp").read(),
                                 language="cpp")
        compile_code(c1)
        compile_code(c2)
        self.assertEqual(c1.is_compiled, 1, c1.compiler_message)
        self.assertEqual(c2.is_compiled, 1, c2.compiler_message)
        a, b = run_two_programs(c2, c1, 1)
        # print(a.time_consumption, a.return_code, a.raw_output)
        # print(b.time_consumption, b.return_code, b.raw_output)
        for output in RunningReport.objects.all():
            print(output.pk, output.return_code, output.time_consumption, output.finish_time)
