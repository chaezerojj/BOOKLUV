<template>
  <div class="wrap">
    <h1>카카오 로그인</h1>

    <button class="kakao" type="button" @click="onKakaoLogin">
      카카오로 로그인
    </button>

    <div class="etc">
      <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const onKakaoLogin = () => {
  authStore.startKakaoLogin();
};
</script>

<style scoped>
.wrap { padding: 24px; }
.kakao {
  padding: 12px 16px;
  border: 0;
  border-radius: 10px;
  cursor: pointer;
}
.etc { margin-top: 12px; }
</style>
