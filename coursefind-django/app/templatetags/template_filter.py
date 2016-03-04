from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_attr(obj, key):
    return obj.__dict__.get(key)
