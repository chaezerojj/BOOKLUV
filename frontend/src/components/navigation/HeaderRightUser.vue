<template>
  <div class="header-right-user">
    <RouterLink :to="{ name: 'alarm' }" @click="onBellClick">
      <div class="bell-wrap">
        <img src="@/assets/images/notification_bell.png" alt="notification-bell" class="notification-bell">
        <span v-if="store.unread" class="badge-dot"></span>
      </div>
    </RouterLink>
    <UserMenu />
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue';
import { RouterLink } from 'vue-router';
import UserMenu from './UserMenu.vue';
import { useKluvChatStore } from '@/stores/kluvChat';

const store = useKluvChatStore();

const onBellClick = () => {
  store.markAlarmsRead();
};

onMounted(() => {
  // keep alarms state up-to-date from header
  store.fetchTodayMeetings();
  store.fetchMeetingAlertLogs();
  store.connectMeetingAlertsSocket();
});

onBeforeUnmount(() => {
  store.disconnectMeetingAlertsSocket();
});
</script>


<style scoped>
.header-right-user {
  display: flex;
  margin: 1.5rem;
  margin-right: 3rem;
  width: 80px;
  align-items: center;
  justify-content: space-between;
}

.notification-bell {
  width: 20px;
}

.bell-wrap {
  position: relative;
  display: inline-block;
}

.badge-dot {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 10px;
  height: 10px;
  background: red;
  border-radius: 999px;
  border: 2px solid #fff;
}
</style>