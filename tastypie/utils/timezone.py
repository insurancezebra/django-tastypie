from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings

try:
    from pytz import AmbiguousTimeError
except ImportError:
    pytz = None

try:
    from django.utils import timezone

    def make_aware(value):
        if getattr(settings, "USE_TZ", False) and timezone.is_naive(value):
            default_tz = timezone.get_default_timezone()
            try:
                value = timezone.make_aware(value, default_tz)
            except AmbiguousTimeError:
                try:
                    _localize = default_tz.localize
                except AttributeError:
                    value = value.replace(tzinfo=default_tz)
                else:
                    value = min(_localize(value, is_dst=True), _localize(value, is_dst=False))
        return value

    def make_naive(value):
        if getattr(settings, "USE_TZ", False) and timezone.is_aware(value):
            default_tz = timezone.get_default_timezone()
            value = timezone.make_naive(value, default_tz)
        return value

    def now():
        d = timezone.now()

        if d.tzinfo:
            return timezone.localtime(timezone.now())

        return d
except ImportError:
    now = datetime.datetime.now
    make_aware = make_naive = lambda x: x


def aware_date(*args, **kwargs):
    return make_aware(datetime.date(*args, **kwargs))


def aware_datetime(*args, **kwargs):
    return make_aware(datetime.datetime(*args, **kwargs))
