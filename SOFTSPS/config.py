import logging

default_log_format = "%(asctime)s| %(levelname)s: %(message)s"

config = {
    "config_path" : "./config/",
    "logformat"   : default_log_format,
    "loglevel"    : logging.INFO,
    "logfile"     : None,
}
