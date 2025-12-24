// src/stores/kluvChat.js
import { defineStore } from "pinia";
import { chatApi } from "@/api/chat";
import { useAuthStore } from "@/stores/auth";

function wsBaseUrlFromApiBase() {
  const apiBase = import.meta.env.VITE_API_BASE_URL;
  // 예: https://bookluv-production.up.railway.app  -> wss://bookluv-production.up.railway.app
  const u = new URL(apiBase);
  const wsProto = u.protocol === "https:" ? "wss:" : "ws:";
  return `${wsProto}//${u.host}`;
}

function fmtTime(ts) {
  if (!ts) return "";
  try {
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return String(ts);
  }
}

export const useKluvChatStore = defineStore("kluvChat", {
  state: () => ({
    // rooms
    roomsLoading: false,
    roomsError: null,
    rooms: [],

    // room detail
    roomLoading: false,
    roomError: null,
    room: null, // {slug,name}
    meeting: null,
    canChat: false,
    currentUser: null,
    leader: null,

    messages: [], // {type, username, message, timestamp, user_id}
    participants: [], // {id, nickname, online, isLeader?}

    // ws
    socket: null,
    socketStatus: "idle", // idle | connecting | open | closed | error
    lastErrorMessage: null,

    // alarms
    alarmsLoading: false,
    alarmsError: null,
    meetingAlerts: [], // [{meeting_id,title,started_at,join_url, room_slug?}]
    unread: false,
    alertsSocket: null,
    alertsStatus: "idle",
    shownMeetingIds: new Set(),
  }),

  actions: {
    // -----------------------------
    // Rooms list
    // -----------------------------
    async fetchRooms() {
      this.roomsLoading = true;
      this.roomsError = null;
      try {
        const data = await chatApi.fetchRooms();
        this.rooms = data.rooms ?? [];
      } catch (e) {
        this.roomsError = e;
        this.rooms = [];
      } finally {
        this.roomsLoading = false;
      }
    },

    // -----------------------------
    // Room detail (REST)
    // -----------------------------
    async fetchRoomDetail(roomSlug) {
      this.roomLoading = true;
      this.roomError = null;

      this.room = null;
      this.meeting = null;
      this.canChat = false;
      this.currentUser = null;
      this.leader = null;
      this.messages = [];
      this.participants = [];

      try {
        const data = await chatApi.fetchRoomDetail(roomSlug);

        this.room = data.room;
        this.meeting = data.meeting ?? null;
        this.canChat = !!data.can_chat;
        this.currentUser = data.current_user ?? null;
        this.leader = data.leader ?? null;

        this.participants = (data.participants ?? []).map((p) => ({
          id: p.id,
          nickname: p.nickname,
          online: !!p.online,
          isLeader: !!p.isLeader || (this.leader?.id != null && p.id === this.leader.id),
        }));

        // messages는 Redis 형식 그대로 올 수도 있어서 최소 정규화
        this.messages = (data.messages ?? []).map((m) => ({
          type: m.type ?? "chat",
          username: m.username ?? m.nickname ?? "Unknown",
          message: m.message ?? "",
          timestamp: m.timestamp ?? null,
          user_id: m.user_id ?? null,
        }));
      } catch (e) {
        this.roomError = e;
      } finally {
        this.roomLoading = false;
      }
    },

    // -----------------------------
    // WebSocket: room
    // -----------------------------
    connectRoomSocket(roomSlug) {
      this.disconnectRoomSocket();

      const authStore = useAuthStore();
      if (!authStore?.isAuthenticated) {
        this.socketStatus = "error";
        this.lastErrorMessage = "로그인 후 채팅에 참여할 수 있어요.";
        return;
      }

      this.socketStatus = "connecting";
      const wsBase = wsBaseUrlFromApiBase();
      const url = `${wsBase}/ws/chat/${roomSlug}/`;
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
            user_id: data.user_id ?? null,
          });
          return;
        }

        if (data.type === "participants") {
          const incoming = Array.isArray(data.participants) ? data.participants : [];
          const leaderId = this.leader?.id ?? null;

          const mapped = incoming.map((p) => ({
            id: p.id,
            nickname: p.nickname ?? p.username ?? "Unknown",
            online: !!p.online,
            isLeader: leaderId != null && p.id === leaderId,
          }));

          // leader first
          mapped.sort((a, b) => (b.isLeader ? 1 : 0) - (a.isLeader ? 1 : 0));
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
      const msg = (text ?? "").trim();
      if (!msg) return;
      if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;
      this.socket.send(JSON.stringify({ message: msg }));
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
    // Alarms: REST + WS
    // -----------------------------
    async fetchTodayMeetings() {
      this.alarmsLoading = true;
      this.alarmsError = null;
      try {
        const data = await chatApi.fetchTodayMeetings();
        const list = data.meetings ?? [];

        // 최신이 위로
        this.meetingAlerts = list.map((x) => ({
          meeting_id: x.meeting_id,
          title: x.title,
          started_at: x.started_at,
          join_url: x.join_url ?? "#",
        }));

        this.unread = this.meetingAlerts.length > 0;
      } catch (e) {
        this.alarmsError = e;
        this.meetingAlerts = [];
      } finally {
        this.alarmsLoading = false;
      }
    },

    connectMeetingAlertsSocket() {
      this.disconnectMeetingAlertsSocket();
      this.alertsStatus = "connecting";

      const wsBase = wsBaseUrlFromApiBase();
      const url = `${wsBase}/ws/meeting-alerts/`;
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
          meeting_id: data.meeting_id,
          title: data.title,
          started_at: data.started_at,
          join_url: data.join_url ?? "#",
        });

        this.unread = true;

        if (this.meetingAlerts.length > 10) {
          this.meetingAlerts = this.meetingAlerts.slice(0, 10);
        }
      };
    },

    markAlarmsRead() {
      this.unread = false;
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

    // helper
    fmtTime,
  },
});
