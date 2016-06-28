#!/usr/bin/env python

"""
generate report as dict
save report as jsonpickle
add option to openqa_review to save/output content as json instead of markdown, could be yaml, too

for every unlabeled issue investigate

# investigate
based on https://progress.opensuse.org/projects/openqav3/wiki/Wiki#Further-decision-steps-working-on-test-issues

* product changes
use command like
env arch=s390x old=1616 new=1621 base=Beta2 vimdiff http://xcdchk.suse.de/browser/data/SLE-12-SP2-Server/Build${old}/${arch}/ChangeLog-${base}-Build${old}.txt http://xcdchk.suse.de/browser/data/SLE-12-SP2-Server/Build${new}/${arch}/ChangeLog-${base}-Build${new}.txt

also check for existance of satsolver reports, e.g. http://xcdchk.suse.de/browser/data/SLE-12-SP3-Desktop/OLD/Build0209/x86_64/SATSOLVER.short.txt which can
shortcut the detection process. It seems if the file exists we already know what's wrong, where the installation would fail

* test software changes
tricky, we don't yet have a git commit for the revision of the tests distribution used, see https://github.com/os-autoinst/os-autoinst/pull/393

   changes in test setup, e.g. our test hardware equipment behaves different or the network

   changes in test infrastructure software, e.g. os-autoinst, openQA

   changes in test management configuration, e.g. openQA database settings

   changes in the test software itself, e.g. read out TEST_GIT_HASH and NEEDLES_GIT_HASH from vars.json from each job and call `git log <old>..<new>` on it
"""
# Python 2 and 3: easiest option
# see http://python-future.org/compatible_idioms.html
from __future__ import absolute_import
from future.standard_library import install_aliases  # isort:skip to keep 'install_aliases()'
install_aliases()
from future.utils import iteritems

import argparse
import difflib
import pprint
import requests
import sys


# http://stackoverflow.com/a/38405539/5031322 inspired by unittest library
def diff_dicts(a, b):
    if a == b:
        return ''
    return '\n'.join(
        difflib.ndiff(pprint.pformat(a, width=30).splitlines(),
                      pprint.pformat(b, width=30).splitlines())
    )

def investigate(args):
    verbose_to_log = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARN,
        3: logging.INFO,
        4: logging.DEBUG
    }
    logging_level = logging.DEBUG if args.verbose > 4 else verbose_to_log[args.verbose]
    log.setLevel(logging_level)
    log.debug("args: %s" % args)
    last_good = requests.get(args.host + '/api/v1/jobs/' + args.last_good).json()['job']
    current = requests.get(args.host + '/api/v1/jobs/' + args.first_bad).json()['job']
    print(diff_dicts(last_good, current))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=CustomFormatter)
    parser.add_argument('-v', '--verbose',
                        help="Increase verbosity level, specify multiple times to increase verbosity",
                        action='count', default=1)
    parser.add_argument('--host', default='https://openqa.opensuse.org',
                        help='openQA host to access')
    parser.add_argument('--first-bad', help='job id of job to investigate')
    parser.add_argument('--last-good', help='Like --first-bad but job id of last good')
    args = parser.parse_args()
    return args


def main():  # pragma: no cover, only interactive
    args = parse_args()
    investigate(args)


if __name__ == "__main__":
    main()
