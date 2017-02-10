''' forms, mostly used for simple tastypie validation '''
from django.contrib.gis import forms


class MeetingForm(forms.Form):
    ''' form for meetings '''
    day_of_week = forms.IntegerField(min_value=1, max_value=7)
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=255, required=False)
    address = forms.CharField(max_length=300)
