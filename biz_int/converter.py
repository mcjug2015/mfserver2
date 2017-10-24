''' converts json dicts to our meeting objects '''
from datetime import datetime, timedelta
from django.contrib.gis.geos.geometry import GEOSGeometry
from django_app.models import Meeting


def meeting_guide_convert(json_obj):
    ''' converts a meeting guide meeting dict into our meeting '''
    meeting = Meeting()
    meeting.name = json_obj["name"]
    meeting.start_time = datetime.strptime(json_obj["time"], '%H:%M')
    meeting.end_time = meeting.start_time + timedelta(hours=1)
    meeting.day_of_week = int(json_obj["day"]) + 1
    meeting.description = json_obj["location"]
    meeting.address = json_obj["formatted_address"]
    meeting.geo_location = GEOSGeometry("POINT(%s %s)" % (json_obj["latitude"], json_obj["longitude"]),
                                        srid=4326)
    return meeting


NAME_TO_CONVERTER = {"meeting_guide": meeting_guide_convert}


def get_meeting_guide_meetings(meeting_dicts):
    ''' get a list of our meeting objs for a list of meeting guide meetings '''
    return [meeting_guide_convert(x) for x in meeting_dicts]
