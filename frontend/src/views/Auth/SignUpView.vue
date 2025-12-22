<template>
  <div class="wrap">
    <h1>회원가입</h1>
    <p>현재는 카카오 로그인으로 회원이 자동 생성돼요.</p>

    <button class="kakao" type="button" @click="onKakaoLogin">
      카카오로 시작하기
    </button>

    <div class="etc">
      <RouterLink :to="{ name: 'login' }">로그인으로 돌아가기</RouterLink>
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
