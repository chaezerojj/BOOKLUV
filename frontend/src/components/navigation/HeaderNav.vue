<template>
  <div class="header-nav">
    <RouterLink :to="{name: 'ai-recommend'}">AI 추천</RouterLink>
    <br>
    <RouterLink :to="{name: 'kluvtalk-list'}">모임</RouterLink>
    <br>
    <RouterLink :to="{name: 'board'}">게시판</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


</script>

<style scoped>
.header-nav {
  display: flex;
  width: 380px;
  justify-content: space-between;
}

.header-nav a {
  margin: 1.5rem;
  text-decoration: none;
  color: #1F2328; 
  font-weight: 500;
}

.header-nav a:hover {
  font-weight: 700;
}

</style>