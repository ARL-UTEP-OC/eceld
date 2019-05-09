# -*- coding: utf-8 -*-
"""
Created on ~

@author: Gerardo Cervantes
"""




from parse_json_to_website import create_website

from parse_eceld import parse_eceld
import sys
export_path = sys.argv[1]
sorted_times, sorted_contents, bug_date = parse_eceld(export_path)

create_website(sorted_times, sorted_contents, bug_date)