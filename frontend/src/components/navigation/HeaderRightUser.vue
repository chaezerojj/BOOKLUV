<template>
  <div class="user">
    <span class="email">{{ authStore.user?.email || "카카오 회원" }}</span>
    <button class="logout" type="button" @click="onLogout">로그아웃</button>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const onLogout = async () => {
  await authStore.logout();
  router.push({ name: "home" });
};
</script>

<style scoped>
.user { display: flex; gap: 12px; align-items: center; }
.email { font-size: 14px; }
.logout { cursor: pointer; }
</style>
