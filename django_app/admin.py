''' admin module '''
# pylint: disable=too-few-public-methods, no-self-use
from django import forms
from django.core import validators
from django.http.response import HttpResponseRedirect
from django.contrib.gis import admin
from django_app.models import Meeting, MeetingType, MeetingNotThere


class LatLongWidget(forms.MultiWidget):
    """
        A Widget that splits Point input into two latitude/longitude boxes.
        From http://stackoverflow.com/questions/17021852/latitude-longitude-widget-for-pointfield
    """

    def __init__(self, attrs=None):
        widgets = (forms.TextInput(attrs=attrs),
                   forms.TextInput(attrs=attrs))
        super(LatLongWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        ''' turn the value into a tuple '''
        if value:
            return tuple(reversed(value.coords))
        return (None, None)


class LatLongField(forms.MultiValueField):
    ''' custom field that takes in a lat and long '''
    widget = LatLongWidget
    srid = 4326

    default_error_messages = {
        'invalid_latitude': ('Enter a valid latitude.'),
        'invalid_longitude': ('Enter a valid longitude.'),
    }

    def __init__(self, *args, **kwargs):
        fields = (forms.FloatField(min_value=-90, max_value=90),
                  forms.FloatField(min_value=-180, max_value=180))
        super(LatLongField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        ''' does magic to allow entering text field lat longs '''
        if data_list:
            # Raise a validation error if latitude or longitude is empty
            # (possible if LatLongField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_latitude'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_longitude'])
            # SRID=4326;POINT(1.12345789 1.123456789)
            srid_str = 'SRID=%d' % self.srid
            point_str = 'POINT(%f %f)' % tuple(reversed(data_list))
            return ';'.join([srid_str, point_str])
        return None


class MeetingTypeAdmin(admin.GeoModelAdmin):
    ''' admin for meeting types '''
    list_display = ('short_name', 'name', 'description')
    list_filter = ('short_name', 'name', 'description')
    search_fields = ('short_name', 'name', 'description')


class MeetingNotThereInline(admin.TabularInline):
    ''' inline for meetingnotthere '''
    model = MeetingNotThere
    raw_id_fields = ('user',)


class MapMeetingAdmin(admin.GeoModelAdmin):
    ''' admin for meetings that shows a map '''
    list_display = ('name', 'description', 'address', 'day_of_week', 'start_time',
                    'end_time', 'is_active', 'creator', 'created_date', 'updated_date')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('name', 'description', 'address', 'creator__username')
    raw_id_fields = ('creator',)
    inlines = [MeetingNotThereInline]


class MeetingAdmin(MapMeetingAdmin):
    ''' admin for meetings that shows lat/long fields'''

    def formfield_for_dbfield(self, db_field, **kwargs):  # pylint:disable=arguments-differ
        ''' show fields instead of map '''
        if db_field.name == 'geo_location':
            return LatLongField()
        return super(MeetingAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class MapMeeting(Meeting):
    ''' proxy cigar shop used in the admin model that shows a map. '''
    class Meta(object):
        ''' meta info '''
        proxy = True


class MeetingNotThereAdmin(admin.GeoModelAdmin):
    ''' admin for meeting not theres '''
    list_display = ('meeting', 'request_host', 'resolved', 'user', 'created_date',
                    'updated_date')
    list_filter = ('resolved',)
    search_fields = ('meeting__name', 'request_host', 'user_agent', 'unique_phone_id',
                     'user__username', 'meeting__creator__username')
    raw_id_fields = ('meeting', 'user')
    actions = ['deactivate_resolve']

    def deactivate_resolve(self, request, queryset):
        ''' deactivate the linked meetings and resolve the meeting_not_theres '''
        for not_there in queryset:
            not_there.meeting.is_active = False
            not_there.meeting.save()
            not_there.resolved = True
            not_there.save()
        return HttpResponseRedirect(request.get_full_path())

    deactivate_resolve.short_description = 'Deactivate and resolve selected'


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MapMeeting, MapMeetingAdmin)
admin.site.register(MeetingType, MeetingTypeAdmin)
admin.site.register(MeetingNotThere, MeetingNotThereAdmin)
