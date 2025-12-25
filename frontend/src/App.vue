<template>
  <div class="app">
    <TheHeader />

    <main class="app-main">
      <RouterView />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
// import { onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";

import TheHeader from '@/components/navigation/TheHeader.vue'
import Footer from '@/components/navigation/Footer.vue' 

// const authStore = useAuthStore();

// onMounted(() => {
//   authStore.fetchMe();
// });
</script>

<style scoped>
.app {
  width: 100%;
  margin: 0;
  padding: 0;
  font-family: Pretendard;
  color: #1f2328;
}

:global(html, body) {
  margin: 0;
  height: 100%;
}

:global(body) {
  min-height: 100vh;
  background: linear-gradient(#FDF4DC, #ffffff);
  background-repeat: no-repeat;
  background-attachment: fixed;
}

/* 페이지가 바뀌는 영역 */
.app-main {
  width: 1300px;
  margin: 0 auto;
  min-height: calc(100vh - var(--header-height, 72px) - var(--footer-height, 96px));
  padding-bottom: 24px;
  /* ensure content doesn't touch footer */
}
</style>
