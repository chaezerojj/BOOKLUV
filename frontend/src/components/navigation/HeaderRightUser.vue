<template>
  <div class="header-right-user">
    <RouterLink :to="{name: 'alarm'}">
      <img src="@/assets/images/notification_bell.png" alt="notification-bell" class="notification-bell">
    </RouterLink>
    <UserMenu />
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
import UserMenu from './UserMenu.vue';

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

</style>