''' writes reports '''
import os
import csv


def write_meeting_guide_report(name, results):
    ''' write a meeting guide report '''
    file_handle = open(os.path.join(os.path.dirname(__file__), "res", "report_%s.csv" % name), 'w')
    the_writer = csv.DictWriter(file_handle, fieldnames=sorted(results[0].keys()))
    the_writer.writeheader()
    the_writer.writerows(results)
