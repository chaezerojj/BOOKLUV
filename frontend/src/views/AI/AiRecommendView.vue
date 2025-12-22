<template>
  <div class="ai-recommend">
    <h1>AI로 당신의 취향에 맞는 책과 모임을 찾아드려요!</h1>

      <div>어쩌구 저쩌구 안내 글 궁시렁 궁시렁</div>
      <br>
      <RouterLink :to="{name: 'ai-test'}" class="ai-test-link">
        <div class="test-link-text">🧡 테스트 하러 가기</div>
      </RouterLink>

  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


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
  width: 200px;
  /* height: 50px; */
  margin: 0 auto;
  padding: 1rem;
  text-align: center;
  align-items: center;
  font-weight: 700;
  font-size: 20px;
}

.test-link-text:hover {
  transform: translateY(-2px);
  box-shadow: 2px 2px 1 rgba(161, 161, 161, 0.3);
}

</style>