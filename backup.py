#!/usr/bin/env python
import configparser
import string
import random
import mdllib

# parse the config
 # username
 # password
 # site URL
 # course id to backup



config = configparser.ConfigParser()
config.read('config.cfg')

username = config['DEFAULT']['username']
password = config['DEFAULT']['password']
url = config['DEFAULT']['url']
courseid = config['DEFAULT']['course']
proxies = None
if config['DEFAULT']['http_proxy']:
    proxies = {}
    proxies['http'] = str(config['DEFAULT']['http_proxy'])
    if config['DEFAULT']['https_proxy']:
        proxies['https'] = str(config['DEFAULT']['https_proxy'])

backup_unique_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

# parse CLI options - later

session = mdllib.getLoggedInSession(url, username, password, proxies)
contextid = mdllib.backupCourse(session, url, courseid, backup_unique_string, proxies)
mdllib.downloadBackup(session, url, courseid, contextid, backup_unique_string, proxies)

# logout and destroy the session key