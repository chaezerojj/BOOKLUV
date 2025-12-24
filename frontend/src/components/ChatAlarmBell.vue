<template>
  <div class="alarm-wrap" ref="root">
    <div class="bell" @click="toggle">
      <span class="icon">🔔</span>
      <span v-if="store.unread" class="dot" />
    </div>

    <div v-if="open" class="box">
      <div class="box-head">
        <div class="title">최근 미팅 알람</div>
      </div>

      <div v-if="store.meetingAlerts.length === 0" class="empty">
        새로운 알람이 없습니다.
      </div>

      <div v-else class="items">
        <div v-for="a in store.meetingAlerts" :key="a.meeting_id" class="item">
          <div class="item-title">{{ a.title }}</div>
          <div class="item-sub">
            <span class="time">{{ a.started_at }} 시작</span>
            <a v-if="a.join_url && a.join_url !== '#'" class="link" :href="a.join_url">참여하기</a>
            <span v-else class="disabled">(방 준비중)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useKluvChatStore } from "@/stores/kluvChat";

const store = useKluvChatStore();
const open = ref(false);
const root = ref(null);

const toggle = async () => {
  open.value = !open.value;
  if (open.value) store.markAlarmsRead();
};

const onClickOutside = (e) => {
  if (!root.value) return;
  if (!root.value.contains(e.target)) open.value = false;
};

onMounted(async () => {
  window.addEventListener("click", onClickOutside);
  await store.fetchTodayMeetings();
  store.connectMeetingAlertsSocket();
});

onBeforeUnmount(() => {
  window.removeEventListener("click", onClickOutside);
  store.disconnectMeetingAlertsSocket();
});
</script>

<style scoped>
.alarm-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
}
.bell {
  position: relative;
  cursor: pointer;
  padding: 6px;
  border-radius: 10px;
}
.bell:hover {
  background: rgba(0, 0, 0, 0.04);
}
.icon {
  font-size: 22px;
}
.dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 9px;
  height: 9px;
  background: #ff4d4f;
  border-radius: 999px;
  border: 2px solid #fff;
}

.box {
  position: absolute;
  top: 44px;
  right: 0;
  width: 340px;
  max-height: 420px;
  overflow: auto;
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.10);
  z-index: 1000;
}
.box-head {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f1f1;
}
.title {
  font-weight: 800;
  font-size: 14px;
}
.empty {
  padding: 18px 14px;
  color: #888;
  text-align: center;
}
.items {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.item {
  background: #f5f9ff;
  border-left: 4px solid #1a73e8;
  padding: 10px 10px 10px 12px;
  border-radius: 10px;
}
.item-title {
  font-weight: 800;
  font-size: 14px;
}
.item-sub {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}
.time {
  color: #555;
}
.link {
  color: #1a73e8;
  font-weight: 800;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
.disabled {
  color: #999;
}
</style>
