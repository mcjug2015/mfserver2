''' module for comparing meeting obj with what we have in the db '''
from datetime import timedelta
from django.contrib.gis.measure import D
from django_app.models import Meeting


def get_similar_meetings_day_time(meeting_obj, distance=0.1):
    ''' grabs meetings that are within distance of meeting obj, on the same day and start at a similar time '''
    db_meetings = Meeting.objects.filter(day_of_week=meeting_obj.day_of_week,
                                         start_time__gte=meeting_obj.start_time-timedelta(minutes=20),
                                         start_time__lte=meeting_obj.start_time+timedelta(minutes=20),
                                         geo_location__distance_lte=(meeting_obj.geo_location, D(mi=distance)))
    return db_meetings.count()
