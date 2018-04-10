import time
from django.test import TestCase

from program.models import Code, RunningReport
from .views import run_two_programs, compile_code, run_three_programs

class ProgramTest(TestCase):
    def test_two_programs(self):
        txt = """-1
1
1
0 1
1
1 2
3
2 3
5
3 4
7
4 5
9
5 6
11
6 7
13
7 8
15
8 9
17
9 10
19"""
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
        self.assertEqual(b.raw_output.strip(), txt)

    def test_three_programs(self):
        c1 = Code.objects.create(code=open("program/testdata/int2.cpp").read(),
                                 language="cpp")
        c2 = Code.objects.create(code=open("program/testdata/int2res.cpp").read(),
                                 language="cpp")
        c3 = Code.objects.create(code=open("program/testdata/int2res2.cpp").read(),
                                 language="cpp")
        compile_code(c1)
        compile_code(c2)
        compile_code(c3)
        self.assertEqual(c1.is_compiled, 1, c1.compiler_message)
        self.assertEqual(c2.is_compiled, 1, c2.compiler_message)
        self.assertEqual(c3.is_compiled, 1, c3.compiler_message)
        a, b, c = run_three_programs(c2, c3, c1, 1)
        print(a.time_consumption, a.return_code, a.raw_output)
        print(b.time_consumption, b.return_code, b.raw_output)
        print(c.time_consumption, c.return_code, c.raw_output)
        txt = """-1
1 1 1 1
reader1: 1
reader2: -99
reader1: 2
reader2: -100
reader1: 3
reader2: -101
reader1: 4
reader2: -102
reader1: 5
reader2: -103
reader1: 6
reader2: -104
reader1: 7
reader2: -105
reader1: 8
reader2: -106
reader1: 9
reader2: -107
reader1: 10
reader2: -108"""
        self.assertEqual(c.raw_output.strip(), txt)
