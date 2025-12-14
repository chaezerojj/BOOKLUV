<template>
  <div>
    <p>알림 + 마이페이지 (로그인 시)</p>
    <NotificationBell />
    <UserMenuDropdown />
  </div>
</template>

<script setup>
import NotificationBell from './NotificationBell.vue';
import UserMenuDropdown from './UserMenuDropdown.vue';


</script>

<style scoped>
div {
  background-color: lightblue;
}
</style>