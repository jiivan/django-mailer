VERSION = (0, 1, 0, "alpha")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()

PRIORITY_MAPPING = {
    "high": "1",
    "medium": "2",
    "low": "3",
    "deferred": "4",
}

# replacement for django.core.mail.send_mail

def send_mail(subject, message, from_email, recipient_list, priority="medium",
              fail_silently=False, auth_user=None, auth_password=None, content_type='text/plain'):
    from django.utils.encoding import force_unicode
    from mailer.models import Message
    from mailer.models import MIME_TYPES
    try:
        content_type = [k for k,v in dict(MIME_TYPES).items() if v == content_type][0]
    except (KeyError, ValueError):
        content_type = '1'
    print content_type
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    priority = PRIORITY_MAPPING[priority]
    for to_address in recipient_list:
        Message(to_address=to_address,
                from_address=from_email,
                subject=subject,
                message_body=message,
                priority=priority,
                content_type=content_type).save()

def mail_admins(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from mailer.models import Message
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.ADMINS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_body=message,
                priority=priority).save()

def mail_managers(subject, message, fail_silently=False, priority="medium"):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from mailer.models import Message
    priority = PRIORITY_MAPPING[priority]
    for name, to_address in settings.MANAGERS:
        Message(to_address=to_address,
                from_address=settings.SERVER_EMAIL,
                subject=settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                message_body=message,
                priority=priority).save()
