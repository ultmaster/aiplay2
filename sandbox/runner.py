import os
import signal
import sys
import time
import threading
import resource

from sandbox.lang import RUNNER_CONFIG


class Runner(object):
    """
    Most Simple Version of a sandbox (with limitation on time and output)
    This is will execute a limited commands (with builtin programming languages)
    """

    @staticmethod
    def run(lang, workspace, add_args=list(), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, time_limit=10):
        """
        :param lang: programming language
        :param workspace: working directory
        :param add_args: additional command arguments
        :param stdin: file handler
        :param stdout: file handler
        :param stderr: file handler
        :param time_limit: int
        :return: dict, {
            "time":
            "exit_code":
        }
        """
        cmd = [RUNNER_CONFIG[lang]["execute_file"]] + RUNNER_CONFIG[lang].get("execute_args", []) + add_args
        child_pid = os.fork()

        if child_pid == 0:
            # in the child now
            try:
                os.setpgrp()
                os.chdir(workspace)
                MAX_OUTPUT = 256 * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_CPU, (time_limit, time_limit))
                resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT, MAX_OUTPUT))
                os.dup2(stdin.fileno(), 0)
                os.dup2(stdout.fileno(), 1)
                os.dup2(stderr.fileno(), 2)
                os.execve(cmd[0], cmd, {})
            except:
                os._exit(-777)  # Magic number, indicates something wrong during execution
        else:
            killer = threading.Timer(time_limit * 5, os.killpg, (child_pid, signal.SIGKILL))
            killer.start()

            pid, status, rusage = os.wait4(child_pid, os.WSTOPPED)

            if killer: killer.cancel()

            result = {"time": rusage.ru_utime + rusage.ru_stime,
                      "exit_code": os.WEXITSTATUS(status)}

            return result
