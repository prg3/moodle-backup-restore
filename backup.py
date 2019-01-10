#!/usr/bin/env python
import configparser
import requests

# parse the config
 # username
 # password
 # site URL
 # course id to backup

proxies = {
  'http': 'localhost:8888',
  'https': 'localhost:8888',
}


config = configparser.ConfigParser()
config.read('config.cfg')

username = config['DEFAULT']['username']
password = config['DEFAULT']['password']
url = config['DEFAULT']['url']

# parse CLI options - later

# Get a session key from the site
# First get a session cookie
r = requests.session()

r.get(url + "/", verify=False, proxies=proxies)
login_payload = {'username': username, 'password': password, 'anchor': ''}
r.post(url + "/login/index.php", data=login_payload,  verify=False, proxies=proxies)
check = r.get(url + "/my/", verify=False, proxies=proxies, allow_redirects=False)

if check.status_code != 200:
    print("Failed login")
else:  
    print("Login successful")


# Hit the first backup form

# Hit the second one

# Download the backup file

# logout and destroy the session key