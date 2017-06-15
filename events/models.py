from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    """
    The event field generally stores a jQuery event JSON object.
    """
    event = JSONField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.event.get('type'), self.user)

    class Meta:
        ordering = ['-created']
