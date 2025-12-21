from django.db import models
from django.utils.text import slugify
from klub_talk.models import Meeting
from channels.db import database_sync_to_async

class Room(models.Model):
    name = models.CharField(max_length=255)
    meeting = models.OneToOneField(
        Meeting, on_delete=models.CASCADE, related_name="room", null=True, blank=True
    )
    slug = models.SlugField(unique=True, blank=True)

        
class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    nickname = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']