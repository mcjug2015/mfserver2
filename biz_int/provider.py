''' provides lists of meeting jsons from res or online '''
import os
import json
from biz_int import grabber


NAME_TO_URL = {"meeting_guide_sanjose": "https://aasanjose.org/wp-admin/admin-ajax.php?action=meetings"}


def get_meeting_guide_sanjose():
    ''' gets the meeting guide san jose list '''
    return get_by_name("meeting_guide_sanjose")


def get_by_name(name):
    ''' get by name from res or pull from web '''
    the_path = os.path.join(os.path.dirname(__file__), "res", "%s.json" % name)
    if not os.path.exists(the_path):
        grabber.get_json(NAME_TO_URL[name], "%s.json" % name)
    return json.loads(open(the_path).read())
