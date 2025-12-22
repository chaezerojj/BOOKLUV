<template>
  <div class="header-right">
    <HeaderRightGuest v-if="authStore.isReady && !authStore.isAuthenticated" />
    <HeaderRightUser v-else-if="authStore.isReady && authStore.isAuthenticated" />
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import HeaderRightGuest from "./HeaderRightGuest.vue";
import HeaderRightUser from "./HeaderRightUser.vue";

const authStore = useAuthStore();
</script>

<style scoped>
.header-right { display: flex; }
</style>
