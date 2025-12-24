<!-- src/components/ChatAlarmBell.vue -->
<template>
  <div class="page">
    <div class="card">
      <div class="head">
        <h3 class="title">최근 미팅 알람</h3>

        <button class="refresh" type="button" @click="onRefresh" :disabled="store.alarmsLoading">
          {{ store.alarmsLoading ? "불러오는 중..." : "새로고침" }}
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
            <div class="time">{{ a.started_at }} 시작</div>
          </div>

          <div class="right">
            <!-- room_slug 있으면 항상 입장 가능 -->
            <RouterLink
              v-if="a.room_slug"
              class="enter"
              :to="{ name: 'kluvtalk-chat-room', params: { roomSlug: a.room_slug } }"
              @click="store.markAlarmsRead()"
            >
              채팅방 입장
            </RouterLink>

            <!-- room_slug 없으면 안내만 -->
            <span v-else class="waiting">방 생성 대기</span>
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

const onRefresh = async () => {
  await store.fetchTodayMeetings();
};

onMounted(async () => {
  await store.fetchTodayMeetings();
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
  width: 520px;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #eee;
  box-shadow: 0 12px 24px rgba(0,0,0,0.06);
  padding: 16px;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.title {
  margin: 0;
  font-size: 15px;
  font-weight: 900;
}

.refresh {
  border: 1px solid #e6e6e6;
  background: #fff;
  padding: 8px 12px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 800;
}
.refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
</style>
