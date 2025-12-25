// src/stores/kluvChat.js
import { defineStore } from "pinia";
import { chatApi } from "@/api/chat";
import { useAuthStore } from "@/stores/auth";

// -----------------------------
// helpers
// -----------------------------
function wsBaseUrl() {
  // ✅ WS base를 env로 분리 (우선순위: VITE_WS_BASE_URL > API_BASE로 계산)
  const explicit = import.meta.env.VITE_WS_BASE_URL;
  if (explicit) return explicit.replace(/\/+$/, "");

  const apiBase = import.meta.env.VITE_API_BASE_URL;
  const u = new URL(apiBase);
  const wsProto = u.protocol === "https:" ? "wss:" : "ws:";
  return `${wsProto}//${u.host}`;
}

function isRailwayHost(host) {
  return String(host || "").includes("railway.app");
}

function shouldSkipAlertsWSInDev() {
  // ✅ 로컬 개발(DEV) + API가 railway면: 세션쿠키/WS 인증 문제로 실패가 흔해서 스킵
  // 필요하면 VITE_ENABLE_ALERTS_WS=true 로 강제 활성화 가능
  const force = String(import.meta.env.VITE_ENABLE_ALERTS_WS || "").toLowerCase() === "true";
  if (force) return false;

  if (!import.meta.env.DEV) return false;

  try {
    const apiBase = import.meta.env.VITE_API_BASE_URL;
    const u = new URL(apiBase);
    return isRailwayHost(u.host);
  } catch {
    return false;
  }
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

function parseRoomSlug(joinUrl) {
  if (!joinUrl || joinUrl === "#") return null;
  // 예: /api/v1/chat/rooms/some-slug-12/
  const m = String(joinUrl).match(/\/chat\/rooms\/([^/]+)\/?$/);
  return m ? m[1] : null;
}

function normalizeMeetingAlert(x) {
  const joinUrl = x?.join_url ?? x?.joinUrl ?? "#";
  return {
    meeting_id: x?.meeting_id ?? x?.meetingId ?? null,
    title: x?.title ?? "",
    started_at: x?.started_at ?? x?.startedAt ?? "",
    join_url: joinUrl,
    created_at: x?.created_at ?? x?.createdAt ?? null,
    room_slug: x?.room_slug ?? x?.roomSlug ?? parseRoomSlug(joinUrl),
  };
}

// Set 대신 배열(직렬화 안전)
function hasId(arr, id) {
  return arr.includes(id);
}
function addId(arr, id) {
  if (id == null) return arr;
  if (arr.includes(id)) return arr;
  return [...arr, id];
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
    room: null,
    meeting: null,
    canChat: false,
    currentUser: null,
    leader: null,

    messages: [],
    participants: [],

    // ws (room)
    socket: null,
    socketStatus: "idle", // idle | connecting | open | closed | error
    lastErrorMessage: null,

    // alarms
    alarmsLoading: false,
    alarmsError: null,
    meetingAlerts: [],
    meetingAlertLogs: [],
    unread: false,

    // ws (alerts)
    alertsSocket: null,
    alertsStatus: "idle",
    shownMeetingIds: [],
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
        this.rooms = data.rooms ?? data ?? [];
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

        this.room = data.room ?? data;
        this.meeting = data.meeting ?? null;
        this.canChat = !!(data.can_chat ?? this.room?.can_chat ?? false);
        this.currentUser = data.current_user ?? null;
        this.leader = data.leader ?? null;

        this.participants = (data.participants ?? this.room?.participants ?? []).map((p) => ({
          id: p.id,
          nickname: p.nickname ?? p.username ?? "Unknown",
          online: !!p.online,
          isLeader: !!p.isLeader || (this.leader?.id != null && p.id === this.leader.id),
        }));

        this.messages = (data.messages ?? this.room?.messages ?? []).map((m) => ({
          type: m.type ?? "chat",
          username: m.username ?? m.nickname ?? "Unknown",
          message: m.message ?? m.content ?? "",
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
      const base = wsBaseUrl();
      const url = `${base}/ws/chat/${roomSlug}/`;

      const socket = new WebSocket(url);
      this.socket = socket;

      socket.onopen = () => {
        this.socketStatus = "open";
      };

      socket.onerror = (err) => {
        this.socketStatus = "error";
        this.lastErrorMessage = "채팅 WebSocket 연결 오류가 발생했어요.";
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
            username: data.username ?? "Unknown",
            message: data.message ?? "",
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
        this.meetingAlerts = list.map(normalizeMeetingAlert);
        this.unread = this.meetingAlerts.length > 0;
      } catch (e) {
        this.alarmsError = e;
        this.meetingAlerts = [];
      } finally {
        this.alarmsLoading = false;
      }
    },

    async fetchMeetingAlertLogs() {
      this.alarmsLoading = true;
      this.alarmsError = null;
      try {
        const data = await chatApi.fetchMeetingAlertLogs();
        const list = data.alerts ?? [];
        this.meetingAlertLogs = list.map(normalizeMeetingAlert);
      } catch (e) {
        this.alarmsError = e;
        this.meetingAlertLogs = [];
      } finally {
        this.alarmsLoading = false;
      }
    },

    connectMeetingAlertsSocket() {
      this.disconnectMeetingAlertsSocket();

      // ✅ 로컬 개발에서 Railway WS 실패가 흔해서 기본 스킵(원하면 env로 강제)
      if (shouldSkipAlertsWSInDev()) {
        this.alertsStatus = "closed";
        return;
      }

      // ✅ 로그인 했을 때만 연결
      const authStore = useAuthStore();
      if (!authStore?.isAuthenticated) {
        this.alertsStatus = "error";
        this.alarmsError = "로그인 후 알림을 받을 수 있어요.";
        return;
      }

      this.alertsStatus = "connecting";

      const base = wsBaseUrl();
      const url = `${base}/ws/meeting-alerts/`;
      const socket = new WebSocket(url);
      this.alertsSocket = socket;

      socket.onopen = () => {
        this.alertsStatus = "open";
      };

      socket.onerror = (err) => {
        this.alertsStatus = "error";
        this.alarmsError = "알림 WebSocket 연결 실패";
        console.error(err);
      };

      socket.onclose = () => {
        this.alertsStatus = "closed";
      };

      socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const meetingId = data.meeting_id ?? data.meetingId ?? null;

        if (meetingId != null && hasId(this.shownMeetingIds, meetingId)) return;
        if (meetingId != null) this.shownMeetingIds = addId(this.shownMeetingIds, meetingId);

        const alert = normalizeMeetingAlert(data);
        this.meetingAlerts.unshift(alert);
        this.meetingAlertLogs.unshift(alert);
        this.unread = true;

        if (this.meetingAlerts.length > 10) this.meetingAlerts = this.meetingAlerts.slice(0, 10);
        if (this.meetingAlertLogs.length > 50) this.meetingAlertLogs = this.meetingAlertLogs.slice(0, 50);
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

    fmtTime,
  },
});
