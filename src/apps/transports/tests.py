import os

from distutils.util import strtobool

DEBUG = bool(strtobool(os.getenv("DEBUG", "False")))

print(bool("False"))

print(strtobool("False"))
