# see http://python-future.org/compatible_idioms.html
from future.standard_library import install_aliases  # isort:skip to keep 'install_aliases()'

install_aliases()
import sys
from argparse import Namespace

import pytest
from openqa_review import investigate  # SUT


def test_help():
    sys.argv += '--help'.split()
    with pytest.raises(SystemExit):
        investigate.main()


@pytest.fixture
def args():
    args = Namespace()
    args.verbose = 5
    # args.load = True
    # args.load_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tumblesle/0046_0056_new_release')
    # Enable saving and disable loading if you want to add new test data downloaded from hosts
    #  args.save = True
    #  args.save_dir = args.load_dir
    return args


def test_investigate(args):
    investigate.investigate(args)
