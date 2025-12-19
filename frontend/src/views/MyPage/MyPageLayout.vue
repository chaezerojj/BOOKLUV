<template>
  <div class="mypage-layout">
    <div class="tab-container">
      <RouterLink :to="{ name: 'mypage-info' }" class="tab-link">회원정보 수정</RouterLink>
      <RouterLink :to="{ name: 'mypage-mykluv' }" class="tab-link">나의 KluvTalk</RouterLink>
    </div>
    <div class="mypage-routerview">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.mypage-layout {
  border: 1px solid black;
  display: flex;
  max-width: 1300px;
  margin: 1rem auto;
  text-align: center;
  justify-content: space-evenly;
}

.tab-container {
  display: flex;
  flex-direction: column;
  width: 200px;
  height: 300px;
  margin: 1rem;
  background-color: #ffffff;
}

.tab-link {
  border: 1px solid red;
  text-decoration: none;
  color: #1f2328;
  font-weight: 500;
  align-items: center;
  margin: 3.5rem auto;
}

.tab-link:hover {
  font-weight: 700;
}

</style>
