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
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped>
.mypage-layout {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1.25rem;
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 1.6rem;
  align-items: start;
}

.tab-container {
  /* width: 200px; */
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding: 1.5rem 1rem;
  background: #ffffff;
  border-radius: 12px;
  box-sizing: border-box;
}

.tab-link {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  border-radius: 10px;
  text-decoration: none;
  color: #1f2238;
  font-weight: 500;
  background: transparent;
  transition: background 0.15s ease, font-weight 0.15s ease;
}

/* exact-active만 활성 스타일 적용 */
.tab-link.router-link-exact-active {
  background: #F0F0F0;
  color: #323232;
  font-weight: 700;
}

.tab-link.router-link-active {
/* 효과없음 */
}

.tab-link:hover {
  background: rgba(31, 34, 56, 0.06);
}

.mypage-routerview {
  width: 600px;
  min-height: 420px;
  background: #ffffff;
  border-radius: 12px;
  padding: 1.75rem;
  box-sizing: border-box;
}
</style>
