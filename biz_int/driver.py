''' creates reports and does batch loads based on other meeting sources '''
from biz_int import provider, converter, comparer, reporter


def drive():
    ''' launch current bizint driver '''
    meeting_guide_report()


def meeting_guide_report():
    ''' create a meeting guide report '''
    meeting_dicts = provider.get_meeting_guide_sanjose()
    our_meetings = converter.get_meeting_guide_meetings(meeting_dicts)
    results = []
    for meeting in our_meetings:
        matching_count = comparer.get_similar_meetings_day_time(meeting)
        results.append({"01 name(theirs)": meeting.name,
                        "02 lat(theirs)": meeting.geo_location.y,
                        "03 long(theirs)": meeting.geo_location.x,
                        "04 address(theirs)": meeting.address,
                        "05 start time(theirs)": meeting.start_time.strftime("%H:%M"),
                        "06 day of week(theirs)": meeting.day_of_week,
                        "07 match count(ours)": matching_count})
    reporter.write_meeting_guide_report("sanjose", results)
