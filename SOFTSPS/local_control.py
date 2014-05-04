#!/usr/bin/python3
from heapq    import heappop, heappush
from time     import sleep
from datetime import datetime

import configparser
import logging
import sys

from program import Program
from config  import config



def read_config_fill_queue():
    from glob import glob
    from os import chdir, getcwd
    from os.path import realpath

    global config

    # restore the current directory at the end of the function
    prev_dir = getcwd()
    chdir(config["config_path"])

    path_program_dict = {}
    for config_path in glob("*.conf"):
        config = configparser.ConfigParser()
        config.read(config_path)
        section = config.sections()[0]
        kwargs = dict(config[section])
        kwargs["name"] = section
        try:
            prog_path = realpath(config[section]["path"])
            del kwargs["path"]
        except KeyError:
            logging.error("%s is missing the path configuartion key",
                          config_path)
            continue
        if prog_path in path_program_dict:
            logging.warn("%s in %s has already been referenced by %s",
                         prog_path, config_path,
                         path_program_dict[prog_path].config_document)
        else:
            prog = Program(prog_path, **kwargs)
            path_program_dict[prog.path] = prog
            heappush(priority_queue, prog)

    chdir(prev_dir)


def init():
    default_log_format = "%(asctime)s| %(levelname)s: %(message)s"
    logging.basicConfig(filename = config.get("logfile", None),
                        level    = config.get("loglevel", logging.WARN),
                        format   = config.get("logformat",
                                              default_log_format))


def main():
    init()
    read_config_fill_queue()
    while True:
        prog = heappop(priority_queue)
        prog.run()
        sleep((prog.next_runtime - datetime.now()).total_seconds())
        heappush(priority_queue, prog)


if __name__ == '__main__':
    priority_queue = []
    main()
