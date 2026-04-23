#! python
import os
import sys

os.environ["PYTHONPATH"] = "/tmp/click_pkg"
sys.path.insert(0, "/tmp/click_pkg")

import click

sys.stdout.write("hello from Python %s\n" % (sys.version,))