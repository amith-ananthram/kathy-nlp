from datetime import datetime


def log(variant, log_line):
    print("%s\t%s\t%s" % (datetime.now(), variant, log_line))
