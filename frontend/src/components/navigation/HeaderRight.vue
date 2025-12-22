<template>
  <div class="header-right">
    <HeaderRightGuest v-if="!authStore.isAuthenticated" />
    <HeaderRightUser v-else />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
import HeaderRightGuest from "./HeaderRightGuest.vue";
import HeaderRightUser from "./HeaderRightUser.vue";

const authStore = useAuthStore();

// 새로고침해도 로그인 유지 확인 (세션이면 쿠키로 유지됨)
onMounted(() => {
  authStore.fetchMe();
});
</script>

<style scoped>
.header-right { display: flex; }
</style>
