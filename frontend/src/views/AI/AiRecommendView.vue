<template>
  <div class="ai-recommend">
    <h1>AI로 당신의 취향에 맞는 책과 모임을 찾아드려요!</h1>
    <div class="hint">아래 버튼을 눌러 테스트를 시작하세요</div>

    <RouterLink :to="{ name: 'ai-test' }" class="ai-test-link">
      <div class="test-link-text">❤️ 테스트 하러 가기</div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.ai-recommend {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.ai-test-link {
  text-decoration: none;
  color: #1f2328;
}

.test-link-text {
  background-color: #ffffff;
  border-radius: 10px;
  width: 240px;
  margin: 0 auto;
  padding: 1rem;
  text-align: center;
  font-weight: 700;
  font-size: 18px;
  border: 1px solid #eee;
}

.test-link-text:hover {
  transform: translateY(-2px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.3);
}
</style>
