<template>
  <div style="padding: 24px">
    <h2>로그인 처리 중...</h2>
    <p v-if="error" style="color: red">{{ error }}</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();
const error = ref("");

onMounted(async () => {
  const ok = await authStore.fetchMe();
  if (!ok) {
    error.value = "로그인 확인에 실패했어요. 다시 로그인 해주세요.";
    setTimeout(() => router.replace({ name: "login" }), 800);
    return;
  }
  router.replace({ name: "home" });
});
</script>
