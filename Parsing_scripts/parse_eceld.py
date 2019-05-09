# -*- coding: utf-8 -*-
"""
Created on ~

@author: Gerardo and Laura
"""
import json
import re

def parse_json_file(file_path, description, json_content_tag):
    times = []
    contents = []

    with open(file_path) as file:
        data = json.load(file)
        for click in data:
            times.append(click['start'])
            contents.append(description + ',' + click[json_content_tag])
    return times, contents

#sorts 2 lists based on first list
def sort_list(list1, list2): 
    from operator import itemgetter
#    zipped_pairs = zip(list2, list1) 
#  
#    z = [x for _, x in sorted(zipped_pairs)] 
    z = [list(x) for x in zip(*sorted(zip(list1, list2), key=itemgetter(0)))]
    return z 

def parse_sys_log_file(syslog_path):
    with open(syslog_path) as file:
        content = file.readlines()
        syslog_times = []
        syslog_contents = []
        for line in content:
            times_str = re.sub(r'.*T', '', line) #Removes everything before the character T
            
            times_str = re.sub(r'-.*', '', times_str) #Removes everything before dash
            hours_int = int(times_str[:2])
            hours_str = str(hours_int + 4)
            times_str = hours_str + times_str[2:]
            syslog_times.append('T' + times_str)
            content_str = re.sub(r'.*cwd', 'cwd', line) #Removes everything before dash
            syslog_contents.append('Log,' + content_str)
            
            
        syslog_times = [x.strip() for x in syslog_times] #remove \n
        syslog_contents = [x.strip() for x in syslog_contents] #remove \n
    return syslog_times, syslog_contents
def parse_eceld(export_path):
    syslog_path = export_path + '/raw/snoopy/1556984515_snoopy.txt'
    click_file_path = export_path + '/parsed/pykeylogger/click.JSON'
    timed_file_path = export_path + '/parsed/pykeylogger/timed.JSON'
    key_file_path = export_path + '/parsed/pykeylogger/keypressData.JSON'
    
    click_times, click_contents = parse_json_file(click_file_path, 'Click', 'title')
    timed_times, timed_contents = parse_json_file(timed_file_path, 'Timed', 'title')
    key_times, key_contents = parse_json_file(key_file_path, 'Key', 'content')
    sys_times, sys_contents = parse_sys_log_file(syslog_path)
    
    all_times = click_times + timed_times + key_times + sys_times
    all_contents = click_contents + timed_contents + key_contents + sys_contents
    
    import datetime
    import time
    
    all_times_in_seconds = []
    for times_str in all_times:
        
        times_str = re.sub(r'.*T', 'T', times_str) #Removes everything before the character T
        
        x = time.strptime(times_str.split(',')[0],'T%H:%M:%S')
        seconds = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
        all_times_in_seconds.append(seconds)
    
    if len(all_times) == 0:
        bug_date = '?'
    else:
        bug_date = all_times[0]
        bug_date = re.sub(r'T.*', '', bug_date) #Cleans date
        
    sorted_lists = sort_list(all_times_in_seconds, all_contents)
    return sorted_lists[0], sorted_lists[1], bug_date
