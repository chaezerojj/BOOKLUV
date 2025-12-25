from rest_framework import serializers
from .models import Room, ChatMessage, MeetingAlert


class RoomSerializer(serializers.ModelSerializer):
    # participants는 ManyToMany라서 카운트가 실용적
    participants_count = serializers.IntegerField(source="participants.count", read_only=True)

    # Room 모델에 created_at이 없으니, meeting.created_at을 대신 내려줌(없으면 None)
    created_at = serializers.SerializerMethodField()

    # meeting id도 자주 필요해서 같이 내려주기
    meeting_id = serializers.IntegerField(source="meeting.id", read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "slug",
            "meeting_id",
            "participants_count",
            "created_at",
        ]

    def get_created_at(self, obj):
        # Room 자체 created_at이 없으므로 meeting의 created_at을 대체로 사용
        if obj.meeting and getattr(obj.meeting, "created_at", None):
            return obj.meeting.created_at
        return None


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "room", "nickname", "message", "timestamp"]
        read_only_fields = ["id", "timestamp"]


class MeetingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAlert
        fields = ["id", "meeting", "user", "created_at"]
        read_only_fields = ["id", "created_at"]
