// src/api/chat.js
import { http } from "@/api/http";

/**
 * ⚠️ 전제:
 * - GET /api/v1/chat/rooms/            -> JSON
 * - GET /api/v1/chat/rooms/:slug/      -> JSON
 * - GET /api/v1/chat/alarms/           -> JSON (이미 JsonResponse로 내려줌)
 */

export const chatApi = {
  async fetchRooms() {
    const res = await http.get("/api/v1/chat/api/rooms/", {
      headers: { Accept: "application/json" },
    });
    return res.data;
  },

  async fetchRoomDetail(roomSlug) {
    const res = await http.get(`/api/v1/chat/api/rooms/${roomSlug}/`, {
      headers: { Accept: "application/json" },
    });
    return res.data;
  },

  async fetchTodayMeetings() {
    const res = await http.get("/api/v1/chat/alarms/", {
      headers: { Accept: "application/json" },
    });
    return res.data; // { meetings: [...] }
  },
};