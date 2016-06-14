from django.template.defaulttags import register

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
