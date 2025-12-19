<template>
  <div class="app">
    <TheHeader />
    
    <main class="app-main">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import TheHeader from '@/components/navigation/TheHeader.vue'
</script>

<style scoped>
.app {
  width: 100%;
  margin: 0 auto;
  padding: 0px;
  font-family: Pretendard;
  background-image: linear-gradient(#FDF4DC, #ffffff);
}

/* 페이지가 바뀌는 영역 */
.app-main {
  width: 1300px;
  margin: 0 auto;
  min-height: calc(100vh - var(--header-height, 72px));
}


</style>
