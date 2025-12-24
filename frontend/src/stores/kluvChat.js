// src/stores/kluvChat.js
import { defineStore } from "pinia";
import { chatApi } from "@/api/chat";
import { useAuthStore } from "@/stores/auth";

/**
 * 서버 WS 메시지 타입(consumer 기준)
 * - { type: "chat", message, username, timestamp }
 * - { type: "system", message, timestamp }
 * - { type: "participants", participants: [{id, username, online}] }
 * - { type: "error", message }
 * (participants_status -> "participants"로 내려옴) :contentReference[oaicite:3]{index=3}
 */

function wsBaseUrl() {
  const proto = window.location.protocol === "https:" ? "wss://" : "ws://";
  return proto + window.location.host;
}

function normalizeInitialMessages(rawMessages) {
  // 백엔드가 Redis에 쌓아둔 형태가 프로젝트마다 다를 수 있어서 방어적으로 매핑
  // views.py에서 msg를 json.loads 후 그대로 messages 배열에 append 함 :contentReference[oaicite:4]{index=4}
  if (!Array.isArray(rawMessages)) return [];
  return rawMessages.map((m) => {
    const username = m.username ?? m.nickname ?? "Unknown";
    const message = m.message ?? m.content ?? "";
    const timestamp = m.timestamp ?? null;
    return {
      type: m.type ?? "chat",
      username,
      message,
      timestamp,
    };
  });
}

export const useKluvChatStore = defineStore("kluvChat", {
  state: () => ({
    // rooms list
    roomsLoading: false,
    roomsError: null,
    rooms: [],

    // room detail
    roomLoading: false,
    roomError: null,
    room: null, // { slug, name, can_chat, leader, participants, total_members, joined_members, ... }
    messages: [],
    participants: [],

    // ws
    socket: null,
    socketStatus: "idle", // idle | connecting | open | closed | error
    lastErrorMessage: null,

    // meeting alerts (ws)
    alertsSocket: null,
    alertsStatus: "idle",
    meetingAlerts: [], // {title, started_at, meeting_id, join_url}
    shownMeetingIds: new Set(),
  }),

  actions: {
    // -----------------------------
    // Rooms
    // -----------------------------
    async fetchRooms() {
      this.roomsLoading = true;
      this.roomsError = null;
      try {
        const data = await chatApi.fetchRooms();

        // 기대 형태(추천)
        // { rooms: [{slug,name, started_at, finished_at, meeting_title, can_chat}, ...] }
        this.rooms = data.rooms ?? data ?? [];
      } catch (e) {
        this.roomsError = e;
        this.rooms = [];
      } finally {
        this.roomsLoading = false;
      }
    },

    // -----------------------------
    // Room detail + initial state
    // -----------------------------
    async fetchRoomDetail(roomSlug) {
      this.roomLoading = true;
      this.roomError = null;
      this.room = null;
      this.messages = [];
      this.participants = [];
      try {
        const data = await chatApi.fetchRoomDetail(roomSlug);

        // 기대 형태(추천)
        // {
        //   room: {slug,name},
        //   can_chat: boolean,
        //   leader: {id, nickname},
        //   participants: [{id, nickname, online?}],
        //   total_members, joined_members,
        //   messages: [...]
        // }
        this.room = data.room ?? data;
        this.room.can_chat = data.can_chat ?? this.room.can_chat ?? false;

        const leader = data.leader ?? this.room.leader ?? null;
        const participants = data.participants ?? this.room.participants ?? [];

        // participants를 WS 형태({id, username, online})로 정규화
        const mapped = participants.map((p) => ({
          id: p.id ?? p.user_id?.id,
          username: p.username ?? p.nickname ?? p.user_id?.nickname ?? "Unknown",
          online: p.online ?? false,
        }));

        // leader도 participants에 포함시켜 표시하고 싶으면 여기서 합치기
        if (leader?.id) {
          const leaderItem = {
            id: leader.id,
            username: leader.nickname ?? leader.username ?? "Leader",
            online: mapped.find((x) => x.id === leader.id)?.online ?? false,
            isLeader: true,
          };
          // leader가 participants에 이미 포함돼 있으면 중복 제거
          const withoutDup = mapped.filter((x) => x.id !== leader.id);
          this.participants = [leaderItem, ...withoutDup];
        } else {
          this.participants = mapped;
        }

        const rawMessages = data.messages ?? this.room.messages ?? [];
        this.messages = normalizeInitialMessages(rawMessages);
      } catch (e) {
        this.roomError = e;
      } finally {
        this.roomLoading = false;
      }
    },

    // -----------------------------
    // WebSocket: chat room
    // -----------------------------
    connectRoomSocket(roomSlug) {
      // 이미 연결돼 있으면 끊고 다시
      this.disconnectRoomSocket();

      const authStore = useAuthStore();
      if (!authStore?.isAuthenticated) {
        this.lastErrorMessage = "로그인 후 채팅에 참여할 수 있어요.";
        this.socketStatus = "error";
        return;
      }

      this.socketStatus = "connecting";
      const url = `${wsBaseUrl()}/ws/chat/${roomSlug}/`;
      const socket = new WebSocket(url);
      this.socket = socket;

      socket.onopen = () => {
        this.socketStatus = "open";
      };

      socket.onerror = (err) => {
        this.socketStatus = "error";
        this.lastErrorMessage = "WebSocket 연결 오류가 발생했어요.";
        console.error(err);
      };

      socket.onclose = () => {
        this.socketStatus = "closed";
        // 자동 재연결(발표용 안정)
        // room 페이지가 유지되는 동안만 재연결되게: socket이 still this.socket일 때만
        const current = this.socket;
        setTimeout(() => {
          if (this.socket === current) return; // 이미 새 소켓이 생겼으면 무시
          // 페이지가 살아있으면 재연결
          // (roomSlug는 view에서 다시 connectRoomSocket을 호출하는 방식으로도 OK)
        }, 3000);
      };

      socket.onmessage = (e) => {
        const data = JSON.parse(e.data);

        if (data.type === "system") {
          this.messages.push({
            type: "system",
            message: data.message,
            timestamp: data.timestamp ?? null,
          });
          return;
        }

        if (data.type === "chat") {
          this.messages.push({
            type: "chat",
            username: data.username,
            message: data.message,
            timestamp: data.timestamp ?? null,
          });
          return;
        }

        if (data.type === "participants") {
          // [{id, username, online}]
          const incoming = Array.isArray(data.participants) ? data.participants : [];
          // 기존 leader 표시 유지
          const leaderId = this.participants.find((p) => p.isLeader)?.id;

          const mapped = incoming.map((p) => ({
            id: p.id,
            username: p.username,
            online: !!p.online,
            isLeader: leaderId === p.id,
          }));

          // leader 먼저
          if (leaderId) {
            mapped.sort((a, b) => (b.isLeader ? 1 : 0) - (a.isLeader ? 1 : 0));
          }

          this.participants = mapped;
          return;
        }

        if (data.type === "error") {
          this.lastErrorMessage = data.message ?? "오류가 발생했어요.";
          return;
        }
      };
    },

    sendMessage(text) {
      if (!text?.trim()) return;
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
      this.socket.send(JSON.stringify({ message: text.trim() })); // consumer receive expects {message} :contentReference[oaicite:5]{index=5}
    },

    disconnectRoomSocket() {
      if (this.socket) {
        try {
          this.socket.close();
        } catch (_) {}
      }
      this.socket = null;
      this.socketStatus = "idle";
    },

    // -----------------------------
    // WebSocket: meeting alerts (global-ish)
    // -----------------------------
    connectMeetingAlertsSocket() {
      this.disconnectMeetingAlertsSocket();
      this.alertsStatus = "connecting";

      // 기존 템플릿은 ip를 하드코딩해둠 → Vue에서는 location.host로 가야 함 :contentReference[oaicite:6]{index=6}
      const url = `${wsBaseUrl()}/ws/meeting-alerts/`;
      const socket = new WebSocket(url);
      this.alertsSocket = socket;

      socket.onopen = () => {
        this.alertsStatus = "open";
      };

      socket.onerror = (err) => {
        this.alertsStatus = "error";
        console.error(err);
      };

      socket.onclose = () => {
        this.alertsStatus = "closed";
      };

      socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const meetingId = data.meeting_id;

        if (meetingId != null && this.shownMeetingIds.has(meetingId)) return;
        if (meetingId != null) this.shownMeetingIds.add(meetingId);

        this.meetingAlerts.unshift({
          title: data.title,
          started_at: data.started_at,
          meeting_id: data.meeting_id,
          join_url: data.join_url ?? "#",
        });

        // 너무 많이 쌓이지 않게
        if (this.meetingAlerts.length > 5) {
          this.meetingAlerts = this.meetingAlerts.slice(0, 5);
        }
      };
    },

    disconnectMeetingAlertsSocket() {
      if (this.alertsSocket) {
        try {
          this.alertsSocket.close();
        } catch (_) {}
      }
      this.alertsSocket = null;
      this.alertsStatus = "idle";
    },
  },
});
