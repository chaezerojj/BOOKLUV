# klub_chat/views.py
import json
import redis
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q

from .models import Room
from klub_talk.models import Meeting, Participate

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0


@login_required
def room_list(request):
    """
    ✅ 기본: JSON 반환 (Vue 연동용)
    ✅ 디버그용 HTML: /api/v1/chat/rooms/?format=html
    """
    # (옵션) 기존 POST로 룸 생성 로직 유지
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not Room.objects.filter(name=room_name).exists():
            Room.objects.create(name=room_name, slug=slugify(room_name))
        return redirect("chat:room-list")

    # 현재 유저가 참여 확정된 모임 ID
    participated_meetings = Participate.objects.filter(
        user_id=request.user, result=True
    ).values_list("meeting", flat=True)

    rooms = Room.objects.filter(
        Q(meeting_id__in=participated_meetings) | Q(meeting__leader_id=request.user)
    ).select_related("meeting")

    # ✅ HTML 템플릿 디버그 보고 싶을 때만
    if request.GET.get("format") == "html":
        return render(request, "chat/room_list.html", {"rooms": rooms, "user": request.user})

    # ✅ JSON (Vue가 먹는 값)
    now = timezone.localtime()
    data = []
    for r in rooms:
        meeting = getattr(r, "meeting", None)
        can_chat = False
        started_at = None
        finished_at = None
        meeting_title = None

        if meeting and meeting.started_at and meeting.finished_at:
            start = timezone.localtime(meeting.started_at)
            end = timezone.localtime(meeting.finished_at)
            can_chat = (start <= now <= end)

            started_at = start.strftime("%Y-%m-%d %H:%M")
            finished_at = end.strftime("%Y-%m-%d %H:%M")
            meeting_title = meeting.title

        data.append({
            "id": r.id,
            "slug": r.slug,
            "name": r.name,
            "meeting_title": meeting_title,
            "started_at": started_at,
            "finished_at": finished_at,
            "can_chat": can_chat,
        })

    return JsonResponse({"rooms": data})


@login_required
def room_detail(request, room_name):
    """
    ✅ 기본: JSON 반환 (Vue 연동용)
    ✅ 디버그용 HTML: /api/v1/chat/rooms/<slug>/?format=html
    """
    room = get_object_or_404(Room, slug=room_name)
    meeting = getattr(room, "meeting", None)
    user = request.user

    # 접근 권한 체크(기존 로직 유지)
    if meeting:
        is_participant = meeting.participations.filter(user_id=user, result=True).exists()
        is_leader = meeting.leader_id == user
        if not (is_participant or is_leader):
            # Vue에선 JSON이 낫다
            if request.GET.get("format") == "html":
                return HttpResponseForbidden("채팅방에 접근할 권한이 없습니다.")
            return JsonResponse({"detail": "채팅방에 접근할 권한이 없습니다."}, status=403)
    else:
        if request.GET.get("format") == "html":
            return HttpResponseForbidden("채팅방에 접근할 권한이 없습니다.")
        return JsonResponse({"detail": "채팅방에 접근할 권한이 없습니다."}, status=403)

    # meeting 기반 데이터 계산
    nickname = user.nickname
    can_chat = False
    leader = None
    participants_qs = []
    total_members = 0
    joined_members = 0

    now = timezone.localtime()

    if meeting:
        start = timezone.localtime(meeting.started_at)
        end = timezone.localtime(meeting.finished_at)

        if start <= now <= end:
            can_chat = True

        leader = meeting.leader_id

        participants_qs = (
            meeting.participations
            .filter(result=True)
            .select_related("user_id")
        )

        joined_members = participants_qs.count()
        total_members = joined_members + 1  # 리더 포함

    # Redis 메시지 로드(기존 로직 유지)
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )
    messages_raw = r.lrange(f"chat_{room.slug}", 0, -1)
    messages = []

    for m in messages_raw:
        msg = json.loads(m)
        # timestamp가 있으면 프론트가 보기 좋게 문자열로(기존 유지)
        if "timestamp" in msg:
            try:
                msg["timestamp"] = timezone.localtime(
                    timezone.datetime.fromisoformat(msg["timestamp"])
                ).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        messages.append(msg)

    # ✅ HTML 디버그
    if request.GET.get("format") == "html":
        return render(
            request,
            "chat/room_detail.html",
            {
                "room": room,
                "nickname": nickname,
                "messages": messages,
                "can_chat": can_chat,
                "leader": leader,
                "participants": participants_qs,
                "total_members": total_members,
                "joined_members": joined_members,
            }
        )

    # ✅ JSON (Vue가 바로 쓰는 형태)
    participants = []
    for p in participants_qs:
        participants.append({
            "id": p.user_id.id,
            "nickname": p.user_id.nickname,
        })

    payload = {
        "room": {
            "id": room.id,
            "slug": room.slug,
            "name": room.name,
            "meeting_id": meeting.id if meeting else None,
        },
        "can_chat": can_chat,
        "leader": {
            "id": leader.id,
            "nickname": leader.nickname,
        } if leader else None,
        "participants": participants,  # 리더 제외(프론트에서 leader 따로 합치면 됨)
        "total_members": total_members,
        "joined_members": joined_members,
        "messages": messages,
    }

    return JsonResponse(payload)



@login_required
def today_meetings(request):
    user = request.user
    now = timezone.localtime()

    today_start_local = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end_local = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    today_start_utc = timezone.make_aware(
        today_start_local.replace(tzinfo=None),
        timezone.get_current_timezone()
    ).astimezone(timezone.utc)

    today_end_utc = timezone.make_aware(
        today_end_local.replace(tzinfo=None),
        timezone.get_current_timezone()
    ).astimezone(timezone.utc)

    meetings_today = Meeting.objects.filter(
        started_at__range=(today_start_utc, today_end_utc)
    ).select_related("room")

    filtered_meetings = []
    for m in meetings_today:
        is_leader = m.leader_id == user
        is_participant = m.participations.filter(user_id=user, result=True).exists()
        if is_leader or is_participant:
            filtered_meetings.append(m)

    data = []
    for m in filtered_meetings:
        start_local = timezone.localtime(m.started_at)
        join_url = f"/api/v1/chat/rooms/{m.room.slug}/" if hasattr(m, "room") and m.room else "#"
        data.append({
            "title": m.title,
            "started_at": start_local.strftime("%H:%M"),
            "meeting_id": m.id,
            "join_url": join_url,
        })

    return JsonResponse({"meetings": data})