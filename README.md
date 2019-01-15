# Moodle backup and restore

## Description

This application will help a Moodle teacher or administrator backup individual courses via a CLI on their workstation without having any access to the sever itself.

## Config

config.cfg-template is avaibale to enter the appropriate information into and rename to config.cfg

## Future

- CLI Options
- Allow downloading all courses
- Download by category
- Automated restore of a course
- Cleanup backup file from server after successful download
- Modularize everything better
- Unit tests
- Detect what type of compression was used when downloading.. maybe normalize to gzip if it is zip?