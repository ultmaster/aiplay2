import os

from django.test import TestCase

from . import run, compile


class RunnerTest(TestCase):

    def test_compile(self):
        p = compile("int main() { return 0; }", "cpp")
        self.assertTrue(p["success"])
        p = compile("print a", "py")
        self.assertFalse(p["success"])
        print(p)

    def test_run(self):
        p = compile("int main() { return 0; }", "cpp")
        print(run("cpp", p["workspace"]))
        p = compile("int main() { while (1); }", "cpp")
        print(run("cpp", p["workspace"], time_limit=1))
        p = compile("""
        #include <bits/stdc++.h>
        using namespace std;

        int main () {
            cout << "hello" << endl;
            return 0;
        }
        """, "cpp")
        with open("two", "w") as f:
            print(run("cpp", p["workspace"], stdout=f))
        with open("two", "r") as f:
            self.assertEqual("hello\n", f.read())
        os.remove("two")

