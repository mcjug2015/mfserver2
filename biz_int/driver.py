''' creates reports and does batch loads based on other meeting sources '''
from biz_int import provider, converter


def drive():
    ''' launch current bizint driver '''
    meeting_guide_report()


def meeting_guide_report():
    ''' create a meeting guide report '''
    meeting_dicts = provider.get_meeting_guide_sanjose()
    our_meetings = converter.get_meeting_guide_meetings(meeting_dicts)
    for meeting in our_meetings:
        print(meeting.name)
