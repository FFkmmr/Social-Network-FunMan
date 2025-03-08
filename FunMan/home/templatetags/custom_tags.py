import os
import uuid
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(name='cache_boost')
def cache_boost():
    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'
    return f'v={version}'
