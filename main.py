#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from job import Job
from notifier import MailNotifier, PrintNotifier

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Missing enough arguments, at least 2: user, pass")
        exit(1)
    if 3 < len(sys.argv) < 7:
        print(
            "Missing enough arguments, expect 6: user, pass, mail_host, mail_user, mail_pass, mail_receiver")
        exit(1)
    if len(sys.argv) > 7:
        print("Too many arguments")
        exit(1)

    job = Job(sys.argv[1], sys.argv[2])

    if len(sys.argv) == 3 or "" in sys.argv[3:7]:
        print("running without sending email")
        job.do(PrintNotifier())
    else:
        print("running with sending email")
        job.do(MailNotifier(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))
