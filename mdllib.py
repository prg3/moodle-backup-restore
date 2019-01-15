import requests
import html2text
import re


# Disable insecure warnings for now
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Get a session key from the site
# First get a session cookie
def getLoggedInSession(url, username, password, proxies = None):
    r = requests.session()

    output = r.get(url + "/", verify=False, proxies=proxies)


    login_payload = {'username': username, 'password': password, 'anchor': ''}
    if proxies:
        r.post(url + "/login/index.php", data=login_payload, verify=False, proxies=proxies)
        output = r.get(url + "/my/", verify=False, proxies=proxies, allow_redirects=False)
    else:
        r.post(url + "/login/index.php", data=login_payload, verify=False)
        output = r.get(url + "/my/", verify=False, allow_redirects=False)
    sesskey_data = re.search('\"sesskey\":\"(\w+)\"', output.text)
    if sesskey_data:
        sesskey = re.sub('\"', '', sesskey_data.group(0)).split(":")[1]
    else:
        print("Missing session key")
        exit

    r.cookies.set('sesskey', sesskey)

    if output.status_code != 200:
        print("Failed login")
        return False
    else:  
        print("Login successful")
        return r

# Run the backup
def backupCourse(r, url, id, backup_unique_string, proxies = None):
    backup_settings = {
        'id':id,
        'stage':4,
        # 'sesskey':sesskey,
        '_qf__backup_confirmation_form':1,
        'setting_root_imscc11':1,
        'setting_root_users':0,
        'setting_root_anonymize':0,
        'setting_root_role_assignments':1,
        'setting_root_activities':1,
        'setting_root_blocks':1,
        'setting_root_filters':1,
        'setting_root_comments':1,
        'setting_root_badges':1,
        'setting_root_calendarevents':1,
        'setting_root_userscompletion':0,
        'setting_root_logs':0,
        'setting_root_grade_histories':0,
        'setting_root_questionbank':1,
        'setting_root_groups':1,
        'setting_root_competencies':1,
        'setting_root_filename': backup_unique_string + "-autobackup.mbz",
        'submitbutton':"Perform+backup"
    }

    if proxies:
        result = r.post(url + "/backup/backup.php", data=backup_settings, verify=False, proxies=proxies, allow_redirects=False)
    else:
        result = r.post(url + "/backup/backup.php", data=backup_settings, verify=False, allow_redirects=False)

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

    return contextid
# Download the backup file

def downloadBackup(r, url, courseid, contextid, backup_unique_string, proxies = None):
    if proxies:
        downloadfile = r.get(url + "/pluginfile.php/" + contextid + "/backup/course/" + backup_unique_string + "-autobackup.mbz?forcedownload=1" , verify=False, proxies=proxies, allow_redirects=False)
    else:
        downloadfile = r.get(url + "/pluginfile.php/" + contextid + "/backup/course/" + backup_unique_string + "-autobackup.mbz?forcedownload=1" , verify=False, proxies=proxies, allow_redirects=False)

    targetFilename="backup-" + courseid + ".mbz"
    f = open(targetFilename , 'wb')
    f.write(downloadfile.content)
    f.close()
    print("Downloaded course backup of course %s to %s"%(contextid, targetFilename))
