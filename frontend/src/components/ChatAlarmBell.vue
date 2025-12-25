<!-- src/components/ChatAlarmBell.vue -->
<template>
  <div class="page">
    <div class="card">
      <div class="head">
        <h3 class="title">🔔 최근 미팅 알람 🔔</h3>

        <button class="refresh" type="button" @click="onRefresh" :disabled="store.alarmsLoading"
          :title="store.alarmsLoading ? '불러오는 중...' : '새로고침'" aria-label="새로고침">
          <img src="@/assets/images/replay.png" alt="새로고침" class="replay-icon" />
        </button>
      </div>

      <div v-if="store.alarmsError" class="state error">
        알람을 불러오지 못했어요.
      </div>

      <div v-else-if="store.meetingAlerts.length === 0" class="state empty">
        새로운 알람이 없습니다.
      </div>

      <div v-else class="list">
        <div v-for="a in store.meetingAlerts" :key="a.meeting_id" class="item">
          <div class="left">
            <div class="name">{{ a.title }}</div>
            <div class="time">{{ fmtDate(a.started_at) }} 시작</div>
          </div>

          <div class="right">
            <!-- room_slug 있으면 항상 입장 가능 -->
            <RouterLink v-if="a.room_slug" class="enter"
              :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: a.room_slug } }" @click="store.markAlarmsRead()">
              채팅방 입장
            </RouterLink>

            <!-- room_slug 없으면 안내만 -->
            <span v-else class="waiting">방 생성 대기</span>
          </div>
        </div <!-- 알림 로그(간단히 한줄로 쌓이는 기록) -->
        <div class="logs-head">알림 로그</div>
        <div class="logs">
          <div v-if="store.meetingAlertLogs.length === 0" class="state empty">알림 로그가 없습니다.</div>
          <div v-else class="log-list">
            <div v-for="l in store.meetingAlertLogs" :key="l.created_at + '-' + l.meeting_id" class="log-item">
              <RouterLink v-if="l.room_slug" :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: l.room_slug } }"
                @click="store.markAlarmsRead()">
                <span class="log-time">{{ fmtDate(l.created_at) }}</span>
                <span class="log-title">{{ l.title }}</span>
              </RouterLink>
              <div v-else class="log-row">
                <span class="log-time">{{ fmtDate(l.created_at) }}</span>
                <span class="log-title">{{ l.title }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <p class="hint">※ 채팅방은 시작 10분 전부터 자동 생성돼요. 입장은 가능하지만, 시간 전엔 채팅 입력이 비활성화돼요.</p>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted } from "vue";
import { useKluvChatStore } from "@/stores/kluvChat";

const store = useKluvChatStore();

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const mm = String(d.getMinutes()).padStart(2, '0');
  return `${y}년 ${m}월 ${day}일 ${hh}:${mm}`;
}

const onRefresh = async () => {
  await store.fetchTodayMeetings();
};

onMounted(async () => {
  await store.fetchTodayMeetings();
  await store.fetchMeetingAlertLogs();
  store.connectMeetingAlertsSocket();
});

onBeforeUnmount(() => {
  store.disconnectMeetingAlertsSocket();
});
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 18px 16px 60px;
}

.card {
  width: 700px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #eee;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
  padding: 16px;
  margin: 0 auto;
  margin-top: 3.5rem;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.title {
  margin: 1.5rem 0;
  margin-left: 1rem;
  font-size: 15px;
  font-weight: 900;
  font-size: 18px;
}

.refresh {
  background: none;
  border: none;
  padding: 0;
  margin-left: 8px;
  display: inline-grid;
  place-items: center;
  width: 36px;
  height: 36px;
  cursor: pointer;
}

.refresh:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.replay-icon {
  width: 20px;
  height: 20px;
  display: block;
  transition: transform 160ms ease, opacity 160ms ease;
}

.refresh:hover .replay-icon {
  transform: rotate(-20deg);
}

.refresh:active .replay-icon {
  transform: scale(0.96);
}

.state {
  padding: 12px;
  border-radius: 14px;
  background: #fafafa;
  border: 1px solid #eee;
  color: #666;
  font-size: 13px;
}

.state.error {
  background: #fff5f5;
  border-color: #ffd6d6;
  color: #b42318;
}

.state.empty {
  text-align: center;
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
  gap: 12px;
  padding: 12px;
  border-radius: 14px;
  background: #f6fbff;
  border-left: 4px solid #1a73e8;
  margin-left: 0.5rem;
}

.left .name {
  font-size: 14px;
  font-weight: 900;
}

.left .time {
  margin-top: 4px;
  font-size: 12px;
  color: #666;
}

.enter {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  border-radius: 12px;
  background: #1a73e8;
  color: #fff;
  text-decoration: none;
  font-weight: 900;
  font-size: 13px;
}

.enter:hover {
  filter: brightness(0.97);
}

.waiting {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 12px;
  border-radius: 12px;
  background: #f3f3f3;
  color: #777;
  border: 1px solid #e6e6e6;
  font-weight: 900;
  font-size: 13px;
}

.hint {
  margin: 12px 0 0;
  font-size: 12px;
  color: #888;
}

.logs-head {
  margin-top: 14px;
  font-weight: 900;
  font-size: 13px;
}

.logs {
  margin-top: 8px;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 6px;
}

.log-item,
.log-row {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 8px 10px;
  border-radius: 10px;
  background: #fff;
  border: 1px solid #f0f0f0;
}

.log-time {
  color: #888;
  font-size: 12px;
  width: 120px;
  white-space: nowrap;
}

.log-title {
  font-weight: 700;
}
</style>
