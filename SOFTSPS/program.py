from functools  import total_ordering
from datetime   import datetime, timedelta
from subprocess import Popen

import subprocess as sp
import shlex
import sys
import logging


EXIT_SUCCESS = 0



@total_ordering
class Program:
    def __init__(self, path, **kwargs):

        self.path            = path
        self.name            = kwargs.get("name", "noname")

        args                 = shlex.split(kwargs.get("args", ''))
        self.command         = [path] + args

        self.intervall       = kwargs.get("intervall", None)

        self.config_document = kwargs.get("config_document", None)

        self.process         = None

        if "time" in kwargs:
            self.intervall   = timedelta(seconds=float(kwargs.get("time")))
        else:
            self.intervall   = None

        self.update_next_runtime()


    def __lt__(self, other):
        return self.next_runtime < other.next_runtime


    def __eq__(self, other):
        return self.next_runtime == other.next_runtime


    def update_next_runtime(self):
        if self.intervall:
            self.next_runtime = datetime.now() + self.intervall


    def run(self):
        self.update_next_runtime()

        if self.process:
            if self.process.poll() is None:
                logging.error("%s runtime exceeds its intervall, killing",
                              self.name)
                self.process.kill()
            elif self.process.returncode != EXIT_SUCCESS:
                logging.error("%s returned with error code %s",
                              self.name, self.process.returncode)

        logging.info("running process %s", self.name)
        self.process = Popen(self.command, stdin=sys.stdin, stdout=sys.stdout,
                             stderr=sys.stderr)
