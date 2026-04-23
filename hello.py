#! python
import os
os.environ.PYTHONPATH="/tmp/click_pkg python3"
print(os.environ.PYTHONPATH)
import click
import sys
sys.stdout.write("hello from Python %s\n" % (sys.version,))