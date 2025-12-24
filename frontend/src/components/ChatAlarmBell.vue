<!-- src/components/ChatAlarmBell.vue -->
<template>
  <div class="wrap">
    <div class="panel">
      <div class="head">
        <h3 class="title">최근 미팅 알람</h3>
        <button class="refresh" type="button" @click="refresh">새로고침</button>
      </div>

      <div v-if="store.alarmsLoading" class="state">불러오는 중...</div>
      <div v-else-if="store.alarmsError" class="state error">알람을 불러오지 못했어요.</div>

      <div v-else-if="store.meetingAlerts.length === 0" class="empty">
        새로운 알람이 없습니다.
      </div>

      <div v-else class="list">
        <div v-for="a in store.meetingAlerts" :key="a.meeting_id" class="item">
          <div class="left">
            <div class="name">{{ a.title }}</div>
            <div class="time">{{ a.started_at }} 시작</div>
          </div>

          <RouterLink
            v-if="a.room_slug"
            class="btn"
            :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: a.room_slug } }"
            @click="store.markAlarmsRead()"
          >
            참여하기
          </RouterLink>

          <button v-else class="btn disabled" type="button" disabled>
            방 준비중
          </button>
        </div>
      </div>

      <div class="hint">
        ※ 채팅방은 시작 10분 전부터 자동 생성/노출돼요.
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useKluvChatStore } from "@/stores/kluvChat";

const store = useKluvChatStore();

const refresh = async () => {
  await store.fetchTodayMeetings();
};

onMounted(async () => {
  await store.fetchTodayMeetings();
  store.connectMeetingAlertsSocket();
});
</script>

<style scoped>
.wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px 16px;
}

.panel {
  width: 360px;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 16px;
  box-shadow: 0 10px 22px rgba(0,0,0,0.06);
  padding: 14px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.title {
  margin: 0;
  font-size: 14px;
  font-weight: 900;
}

.refresh {
  border: 1px solid #e5e5e5;
  background: #fafafa;
  border-radius: 10px;
  padding: 6px 10px;
  cursor: pointer;
  font-weight: 700;
}

.state {
  padding: 12px;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 12px;
  font-size: 13px;
}
.state.error {
  background: #fff5f5;
  border-color: #ffd6d6;
  color: #b42318;
}

.empty {
  padding: 18px 10px;
  text-align: center;
  color: #888;
  font-size: 13px;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px;
  border-radius: 12px;
  background: #f7fbff;
  border-left: 4px solid #1a73e8;
}

.name {
  font-size: 13px;
  font-weight: 900;
}
.time {
  margin-top: 2px;
  font-size: 12px;
  color: #666;
}

.btn {
  text-decoration: none;
  background: #1a73e8;
  color: #fff;
  font-weight: 900;
  border-radius: 10px;
  padding: 8px 10px;
  font-size: 12px;
}
.btn:hover {
  opacity: 0.92;
}
.btn.disabled {
  background: #e5e5e5;
  color: #888;
  cursor: not-allowed;
}

.hint {
  margin-top: 10px;
  font-size: 11px;
  color: #888;
}
</style>
