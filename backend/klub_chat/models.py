from django.db import models
from klub_talk.models import Meeting
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=255)
    meeting = models.OneToOneField(
        Meeting, on_delete=models.CASCADE, related_name="room", null=True, blank=True
    )
    slug = models.SlugField(unique=True, blank=True)
    
    def is_meeting_active(self):
        """회의 중이면 True"""
        if not self.meeting:
            return False
        now = timezone.now()
        return self.meeting.started_at <= now <= self.meeting.finished_at

        
class ChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    nickname = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
        
class MeetingAlert(models.Model):
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE)  # unique=True 대신 OneToOneField
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meeting',)  # 중복 알림 방지
