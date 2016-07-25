from django.template.defaulttags import register
import re
try:
    import utilities
except:
    from . import utilities


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_attr(obj, key):
    return obj.__dict__.get(key)

@register.filter
def day_of_week(n):
    try:
        _DAYS = {1: "Monday",
                 2: "Tuesday",
                 3: "Wednesday",
                 4: "Thursday",
                 5: "Friday",
                 6: "Saturday",
                 0: "Sunday"}
        n = n % 7
        return _DAYS[n]
    except:
        return None

@register.filter
def days_of_week(days):
    try:
        return [day_of_week(day) for day in days]
    except:
        return []

@register.filter
def cmu_building(s):
    return utilities.getBuildingText(s)

@register.filter
def url_target_blank(text):
    return re.sub("<a([^>]+)(?<!target=)>", '<a target="_blank"\\1>', text)


@register.filter
def remove_script(text):
    import django.utils.html
    return django.utils.html.remove_tags(text, 'script')
