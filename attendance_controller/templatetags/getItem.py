from django import template

register = template.Library()
@register.filter
def get_percent(dictionary, key):
    subjectAttendance=dictionary.get(key)
    if subjectAttendance[0]!=0:
        return (subjectAttendance[1]/subjectAttendance[0])*100
    else:
        return 100