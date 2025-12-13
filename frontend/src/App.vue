<template>
  <TheHeader />

  <main class="app-main">
    <RouterView />
  </main>
</template>

<script setup>
import { RouterView } from 'vue-router'
import TheHeader from '@/components/navigation/TheHeader.vue'
</script>

<style scoped>
/* 페이지가 바뀌는 영역 */
.app-main {
  min-height: calc(100vh - var(--header-height, 72px));
}
</style>
