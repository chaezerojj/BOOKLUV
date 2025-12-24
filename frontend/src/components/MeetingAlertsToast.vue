<!-- src/components/MeetingAlertsToast.vue -->
<template>
  <div class="toast-wrap" v-if="alerts.length">
    <div class="toast" v-for="a in alerts" :key="a.meeting_id ?? a.title + a.started_at">
      <div class="title">
        <span class="dot" />
        <strong>{{ a.title }}</strong>
      </div>
      <div class="meta">
        <span>{{ a.started_at }} 시작</span>
        <RouterLink class="link" :to="toChatRoom(a.join_url)">참여</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

defineProps({
  alerts: { type: Array, required: true },
});

/**
 * 백엔드 join_url은 템플릿/JsonResponse에서
 * "/api/v1/chat/rooms/<slug>/" 형태로 내려줌 :contentReference[oaicite:7]{index=7}
 * Vue 라우트는 "/kluvtalk/chat/:roomSlug"로 갈 거라서 변환해줌.
 */
const toChatRoom = (joinUrl) => {
  if (!joinUrl || joinUrl === "#") return { name: "kluvtalk-chat-list" };

  const m = String(joinUrl).match(/\/api\/v1\/chat\/rooms\/([^/]+)\/?/);
  if (!m) return { name: "kluvtalk-chat-list" };

  return { name: "kluvtalk-chat-room", params: { roomSlug: m[1] } };
};
</script>

<style scoped>
.toast-wrap {
  position: fixed;
  right: 18px;
  bottom: 18px;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 50;
}

.toast {
  background: #ffffff;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 12px 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #1a73e8;
}

.meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #666;
  font-size: 13px;
}

.link {
  color: #1a73e8;
  text-decoration: none;
  font-weight: 700;
}
.link:hover { text-decoration: underline; }
</style>
