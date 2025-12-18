<template>
  <div class="header-right-guest">
    <!-- <p>회원가입 + 로그인 (비로그인 시)</p> -->
    <RouterLink :to="{name: 'signup'}">회원가입</RouterLink>
    <span>|</span>
    <RouterLink :to="{name: 'login'}">로그인</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


</script>

<style scoped>
.header-right-guest {
  width: 150px;
  display: flex;
  justify-content: space-between;
  margin: auto;
}

.header-right-guest a {
  text-decoration: none;
  color: #1f2328;
  font-weight: 500;
}

.header-right-guest a:hover {
  font-weight: 700;
}


</style>