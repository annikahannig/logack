import uuid

from django.db import models
from django.contrib.auth.models import User


class Sub(models.Model):
    """
    A sub belongs to a user and has credentials for
    API access.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subs")

    name = models.CharField(max_length=60)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    """
    An event belongs to a user and is usually associated with a
    sub.
    """
    # Relations
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events")

    sub = models.ForeignKey(
        Sub,
        on_delete=models.CASCADE,
        related_name="events")

    # Content
    label = models.CharField(max_length=80)
    description = models.CharField(max_length=255)
    
    # State can be unacknowledged (null), positive (true) or
    # rejected (false)
    ack = models.BooleanField(null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Indexes
        indexes = [
            models.Index(fields=["label"]),
        ]

        # Default ordering
        ordering = ["-created_at"]

