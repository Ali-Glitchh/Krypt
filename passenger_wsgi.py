from Krypt import app as application
import sys
import os

INTERP = os.path.expanduser("/usr/local/bin/python3.8")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

application.secret_key = 'your-secret-key-here'