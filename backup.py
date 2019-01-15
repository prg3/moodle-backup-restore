#!/usr/bin/env python
import configparser
import string
import random
import mdllib
import argparse

parser = argparse.ArgumentParser(description='Backs up a course from a Moodle instance')
parser.add_argument('--courseid', metavar='courseid', type=str,
                    help='The ID of the course you wish to back up',
                    default=0)
parser.add_argument('--config', dest='configfile',
                    help='Name of the config file to read',
                    default='config.cfg')

args = parser.parse_args()
configfile = args.configfile
courseid = args.courseid

config = configparser.ConfigParser()
config.read(configfile)

username = config['DEFAULT']['username']
password = config['DEFAULT']['password']
url = config['DEFAULT']['url']
if courseid == 0:
    courseid = config['DEFAULT']['course']
else:
    print("Course ID %s specified by CLI option, ignoring course id of %s from config file"%(courseid, (config['DEFAULT']['course'])))
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