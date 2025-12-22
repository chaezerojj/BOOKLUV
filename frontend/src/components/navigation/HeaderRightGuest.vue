<template>
  <div class="guest">
    <RouterLink :to="{ name: 'login' }" class="link">로그인</RouterLink>
    <RouterLink :to="{ name: 'signup' }" class="link">회원가입</RouterLink>
  </div>
</template>

<script setup></script>

<style scoped>
.guest { display: flex; gap: 12px; align-items: center; }
.link { text-decoration: none; }
</style>
