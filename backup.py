#!/usr/bin/env python
import configparser
import requests
import html2text
import re
import string
import random

# Disable insecure warnings for now
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
courseid = config['DEFAULT']['course']

# parse CLI options - later

# Get a session key from the site
# First get a session cookie
r = requests.session()

output = r.get(url + "/", verify=False, proxies=proxies)


login_payload = {'username': username, 'password': password, 'anchor': ''}
r.post(url + "/login/index.php", data=login_payload, verify=False, proxies=proxies)
output = r.get(url + "/my/", verify=False, proxies=proxies, allow_redirects=False)
sesskey_data = re.search('\"sesskey\":\"(\w+)\"', output.text)
if sesskey_data:
    sesskey = re.sub('\"', '', sesskey_data.group(0)).split(":")[1]
else:
    print("Missing session key")
    exit

r.cookies.set('sesskey', sesskey)

if output.status_code != 200:
    print("Failed login")
else:  
    print("Login successful")

# Run the backup
backup_unique_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
backup_settings = {
    'id':courseid,
    'stage':4,
    'sesskey':sesskey,
    '_qf__backup_confirmation_form':1,
    'setting_root_imscc11':1,
    'setting_root_users':0,
    'setting_root_anonymize':0,
    'setting_root_role_assignments':0,
    'setting_root_activities':0,
    'setting_root_blocks':0,
    'setting_root_filters':0,
    'setting_root_comments':0,
    'setting_root_badges':0,
    'setting_root_calendarevents':0,
    'setting_root_userscompletion':0,
    'setting_root_logs':0,
    'setting_root_grade_histories':0,
    'setting_root_questionbank':1,
    'setting_root_groups':1,
    'setting_root_competencies':1,
    'setting_section_section_1_included':1,
    'setting_section_section_1_userinfo':0,
    'setting_activity_forum_1_included':1,
    'setting_activity_forum_1_userinfo':0,
    'setting_section_section_2_included':1,
    'setting_section_section_2_userinfo':0,
    'setting_section_section_3_included':1,
    'setting_section_section_3_userinfo':0,
    'setting_section_section_4_included':1,
    'setting_section_section_4_userinfo':0,
    'setting_section_section_5_included':1,
    'setting_section_section_5_userinfo':0,
    'setting_root_filename': backup_unique_string + "-autobackup.mbz",
    'submitbutton':"Perform+backup"
}

result = r.post(url + "/backup/backup.php", data=backup_settings, verify=False, proxies=proxies, allow_redirects=False)
contextid = 0

if result.status_code != 200:
    print("Failed to run the backup, details below")
    if result.is_redirect:
        print("Redirected to : " + str(result.next.url))
    else:
        print (html2text.html2text(result.text))
else:  
    print("Backup successful")
    contextid_data = re.search('\"contextid\":(\w+)', result.text)
    if contextid_data:
        contextid = re.sub('\"', '', contextid_data.group(0)).split(":")[1]
    else:
        print("Missing context id")
        exit


# Download the backup file

downloadfile = r.get(url + "/pluginfile.php/" + contextid + "/backup/course/" + backup_unique_string + "-autobackup.mbz?forcedownload=1" , verify=False, proxies=proxies, allow_redirects=False)

f = open("backup-" + courseid + ".mbz", 'wb')
f.write(downloadfile.content)
f.close()


# logout and destroy the session key