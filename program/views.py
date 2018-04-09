import os
import fcntl
import pickle
import time
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from django.conf import settings
from django.shortcuts import render

from sandbox import run, compile
from util.timestamp import timestamp_onlydigit
from .models import RunningReport, Code


def compile_code(a: Code):
    p = compile(a.code, a.language)
    if not p["success"]:
        a.is_compiled = 2
    else:
        a.is_compiled = 1
        a.workspace = p["workspace"]
    a.compiler_message = p["message"]
    a.save()


def run_two_programs(a: Code, b: Code, time_limit: int):
    """
    :param a: submitted code
    :param b: interactor (judge)

    judge should follow the following protocol:
    stdin: abandoned
    stdout: report
    arg[1]: read, file descriptor
    arg[2]: write, file descriptor

    possibly arg[3] and arg[4] in run_three_programs
    arg[3]: read, file descriptor
    arg[4]: write, file descriptor

    :return: (RunningReport a, RunningReport b)
    """
    if a.is_compiled != 1 or b.is_compiled != 1:
        raise ValueError("Two programs should be compiled")

    r1, w1 = os.pipe()  # interactor read, submission write
    r2, w2 = os.pipe()  # submission read, interactor write

    report_workspace = os.path.join(settings.DATA_DIR, timestamp_onlydigit())
    os.makedirs(report_workspace, exist_ok=True)
    report_file_path = os.path.join(report_workspace, "report")
    report_model_path = os.path.join(report_workspace, "model")

    report_model_a = RunningReport.objects.create(code=a)
    report_model_b = RunningReport.objects.create(code=b)

    interactor_pid = os.fork()
    if interactor_pid == 0:
        # This is the child process for interactor running usage
        os.close(w1)
        os.close(r2)
        fcntl.fcntl(r1, fcntl.F_SETFD, 0)   # set close-on-exec flag 0
        fcntl.fcntl(w2, fcntl.F_SETFD, 0)

        with open(report_file_path, "w") as report_writer:
            p = run(b.language, b.workspace, add_args=[str(r1), str(w2)], stdout=report_writer, time_limit=time_limit)
        with open(report_file_path, "r") as report_reader:
            report_model_b.raw_output = report_reader.read()
            report_model_b.finish_time = timezone.now()
            report_model_b.time_consumption = p["time"]
            report_model_b.return_code = p["exit_code"]
        with open(report_model_path, "wb") as report_model_writer:
            pickle.dump(report_model_b, report_model_writer)
        os._exit(0)
    else:
        # This is the parent process for submission
        os.close(r1)
        os.close(w2)
        r, w = os.fdopen(r2, 'r'), os.fdopen(w1, 'w')
        p = run(a.language, a.workspace, stdin=r, stdout=w, time_limit=time_limit)
        r.close()
        w.close()
        report_model_a.finish_time = timezone.now()
        report_model_a.time_consumption = p["time"]
        report_model_a.return_code = p["exit_code"]
        report_model_a.save()

        os.wait4(interactor_pid, os.WSTOPPED)
        with open(report_model_path, "rb") as report_model_reader:
            report_model_b = pickle.load(report_model_reader)
            report_model_b.save()

    return report_model_a, report_model_b


def run_three_programs(a: Code, b: Code, c: Code, time_limit: int):
    """
    Basically same as run_two_programs. c is judge
    """
    if a.is_compiled != 1 or b.is_compiled != 1 or c.is_compiled != 1:
        raise ValueError("Three programs should be compiled")

    r1, w1 = os.pipe()  # judge read, code_a write
    r2, w2 = os.pipe()  # code_a read, judge write
    r3, w3 = os.pipe()  # judge read, code_b write
    r4, w4 = os.pipe()  # coee_b read, judge write

    report_workspace = os.path.join(settings.DATA_DIR, timestamp_onlydigit())
    os.makedirs(report_workspace, exist_ok=True)
    report_file_path = os.path.join(report_workspace, "report")
    report_model_a_path = os.path.join(report_workspace, "model_a")
    report_model_b_path = os.path.join(report_workspace, "model_b")

    report_model_a = RunningReport.objects.create(code=a)
    report_model_b = RunningReport.objects.create(code=b)
    report_model_c = RunningReport.objects.create(code=c)

    interactor_pid = os.fork()
    if interactor_pid == 0:
        # Forks two programs to run a and b
        os.close(r1)
        os.close(w2)
        os.close(r3)
        os.close(w4)

        def run_a_and_b(code, report_model, report_model_path,
                        read_pipe, write_pipe, close_pipes):
            for pipe in close_pipes:
                os.close(pipe)
            r, w = os.fdopen(read_pipe, 'r'), os.fdopen(write_pipe, 'w')
            p = run(code.language, code.workspace, stdin=r, stdout=w, time_limit=time_limit)
            r.close()
            w.close()
            report_model.finish_time = timezone.now()
            report_model.time_consumption = p["time"]
            report_model.return_code = p["exit_code"]
            with open(report_model_path, "wb") as report_model_writer:
                pickle.dump(report_model, report_model_writer)
            os._exit(0)

        new_pid = os.fork()
        if new_pid == 0:
            # Code a
            run_a_and_b(a, report_model_a, report_model_a_path, r2, w1, [w3, r4])
        else:
            # Code b
            run_a_and_b(b, report_model_b, report_model_b_path, r4, w3, [w1, r2])
            os.wait4(new_pid, os.WSTOPPED)
    else:
        os.close(w1)
        os.close(r2)
        os.close(w3)
        os.close(r4)
        fcntl.fcntl(r1, fcntl.F_SETFD, 0)
        fcntl.fcntl(w2, fcntl.F_SETFD, 0)
        fcntl.fcntl(r3, fcntl.F_SETFD, 0)
        fcntl.fcntl(w4, fcntl.F_SETFD, 0)

        with open(report_file_path, "w") as report_writer:
            p = run(c.language, c.workspace, add_args=[str(r1), str(w2), str(r3), str(w4)],
                    stdout=report_writer, time_limit=time_limit)
        with open(report_file_path, "r") as report_reader:
            report_model_c.raw_output = report_reader.read()
            report_model_c.finish_time = timezone.now()
            report_model_c.time_consumption = p["time"]
            report_model_c.return_code = p["exit_code"]
            report_model_c.save()

        os.wait4(interactor_pid, os.WSTOPPED)

        with open(report_model_a_path, "rb") as report_model_reader:
            report_model_a = pickle.load(report_model_reader)
            report_model_a.save()
        with open(report_model_b_path, "rb") as report_model_reader:
            report_model_b = pickle.load(report_model_reader)
            report_model_b.save()

    return report_model_a, report_model_b, report_model_c
