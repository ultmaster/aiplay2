import os
import subprocess
from datetime import datetime

from django.conf import settings

from sandbox.lang import RUNNER_CONFIG
from util.timestamp import timestamp_onlydigit


class Compiler(object):

    @staticmethod
    def compile(code, lang):
        now_string = timestamp_onlydigit()
        workspace = os.path.join(settings.DATA_DIR, now_string)
        os.makedirs(workspace, exist_ok=True)
        now_working_space = os.getcwd()
        os.chdir(workspace)
        config = RUNNER_CONFIG[lang]
        with open(config["code_file"], "w") as code_file_writer:
            code_file_writer.write(code)
        try:
            with open("compile.log", "w") as log:
                compile_process = subprocess.run([config["compiler_file"]] + config["compiler_args"],
                                                 stdin=subprocess.DEVNULL, stdout=log, stderr=log, timeout=30)
            try:
                with open("compile.log", "r") as compile_log_reader:
                    compile_log = compile_log_reader.read()
            except FileNotFoundError:
                compile_log = ""
            os.chdir(now_working_space)
            if compile_process.returncode != 0:
                if not compile_log:
                    compile_log = "Compiler returned non-zero exit code, but nothing reported."
                return {
                    "success": False,
                    "message": compile_log
                }
            return {
                "success": True,
                "workspace": workspace,
                "message": compile_log
            }
        except subprocess.TimeoutExpired:
            os.chdir(now_working_space)
            return {
                "success": False,
                "message": "Compilation time limit (30s) is exceeded."
            }
