# Creating daily Tag and commit

import json
import sys
import os
from datetime import datetime

sys.dont_write_bytecode = True


class Tag(object):

    def __init__(self, tag_info_file):
        self.tag_info_file = tag_info_file
        with open(tag_info_file) as f:
            self.info = json.load(f)

    def current_calender_week(self):
        today = datetime.now().date().isocalendar()
        year = today[0]
        week = today[1]
        day = today[2]
	if week < 10:
		week = str(0) + str(week)
		print week
        print "DB" + str(year % 100) + str(week) + str(day)
        return 'DB' + str(year % 100) + str(week) + str(day)

    def get_previouse_tag(self):
        return self.info['VERSION_PREVIOUS']

    def get_current_tag(self):
        current_cw = self.current_calender_week()
        # remove version number (A,B,C)
        previous_cw = self.get_previouse_tag().split('_')[-1][:-1]
        if current_cw != previous_cw:
            # not match means it's new day, need to start from A,
            self.info['VERSION_NUMBER'] = 'A'
            self.info['VERSION_PREVIOUS'] = self.info['VERSION_BASE'] + '_' + current_cw + self.info['VERSION_NUMBER']
        else:
            # for same day, increamental version number is B,C,D
            next_char = chr(ord(self.info['VERSION_NUMBER']) + 1)
            print "next char = " + next_char
            self.info['VERSION_NUMBER'] = str(next_char)
            self.info['VERSION_PREVIOUS'] = self.info['VERSION_BASE'] + '_' + previous_cw + self.info['VERSION_NUMBER']
        return self.info['VERSION_BASE'] + '_' + current_cw + self.info['VERSION_NUMBER']

    def update_tag_info_file(self):
        print "Updating tag info file."
        os.chdir(sys.path[0])
        with open(self.tag_info_file, 'w') as f:
            json.dump(self.info, f, indent=4, sort_keys=True)
