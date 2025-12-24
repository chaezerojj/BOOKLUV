from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from klub_talk.models import Meeting


class Room(models.Model):
    name = models.CharField(max_length=255)
    meeting = models.OneToOneField(
        Meeting, on_delete=models.CASCADE, related_name="room", null=True, blank=True
    )
    slug = models.SlugField(unique=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="rooms")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Room.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def is_meeting_active(self):
        if not self.meeting:
            return False
        now = timezone.now()
        if not self.meeting.started_at or not self.meeting.finished_at:
            return False
        return self.meeting.started_at <= now <= self.meeting.finished_at


class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    nickname = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['room', 'timestamp']),
        ]


class MeetingAlert(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['meeting', 'user'], name='unique_meeting_user')
        ]
