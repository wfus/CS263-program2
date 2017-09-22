#!/usr/bin/env bash

# network_cracker.sh
#
# ==== INSTRUCTIONS FOR USING ANOTHER LANGUAGE ====
#
# You may use another language. However, you are responsible for making sure
# your code works with the following command-line interface:
#
#   your_program <username_to_crack> <url> <port>
#
# Additionally, your program should have the same output and exit code behavior
# as network_cracker.py's main function. That is, the program should exit with
# exit code 1 if unsuccessful. If successful, it should exit with code 0 and
# print the cracked password as the last line of output.
#
# For clarity, please name your source file network_cracker.<language_ext>.
# Also, be sure to change the line below to the appropriate invocation command
# for your language. Finally, add any dependencies to setup.sh.
#
# From past experience, Python is the easiest to use by far for this. To the
# best of my memory, all but one submissions from last year were in Python.

python3 `dirname $0`/network_cracker.py "$@"
