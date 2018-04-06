SUPPORTED_LANG = (
    ('cpp', 'C++'),
    ('java', 'Java'),
    ('py', 'Python'),
    ('js', 'Javascript')
)


RUNNER_CONFIG = {
    "cpp": {
        "compiler_file": "/usr/local/bin/g++-7",
        "compiler_args": ["-O2", "-std=c++11", '-o', "foo", "foo.cc", "-DONLINE_JUDGE", "-lm",
                          "-fmax-errors=3"],
        "code_file": "foo.cc",
        "execute_file": "foo",
    },
    "java": {
        "compiler_file": "/usr/bin/javac",
        "compiler_args": ["-encoding", "utf8", "Main.java"],
        "code_file": "Main.java",
        "execute_file": "/usr/bin/java",
        "execute_args": ["-Xss1M", "-XX:MaxPermSize=16M", "-XX:PermSize=8M", "-Xms16M", "-Xmx{max_memory}M",
                         "-Dfile.encoding=UTF-8", "Main"],
    },
    "py": {
        "compiler_file": "/Library/Frameworks/Python.framework/Versions/3.5/bin/python3",
        "compiler_args": ["-m", "py_compile", "foo.py"],
        "code_file": "foo.py",
        "execute_file": "/Library/Frameworks/Python.framework/Versions/3.5/bin/python3",
        "execute_args": ["foo.py"]
    }
}