<template>
  <div class="ai-recommend">
    <h1 class="ai-main-text">🪄 AI로 취향에 맞는 책과 모임을 찾아드려요! 🪄</h1>
    <div class="img-box">
      <img class="book-3d-img" src="../../assets/images/3dicons-notebook.png" alt="book-3d-img">
      <img class="chat-3d-img" src="../../assets/images/3dicons-chat.png" alt="chat-3d-img">
    </div>
    <div class="text">⬇️아래 버튼을 눌러 테스트를 시작하세요⬇️</div>

    <RouterLink :to="{ name: 'ai-test' }" class="ai-test-link">
      <div class="test-link-text">❤️테스트 하러 가기</div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.ai-recommend {
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
  background: radial-gradient(circle at center, #ffffff 0%, #ffffff 20%, #FDF4DC 100%, 0.7);
}

.ai-main-text {
  padding: 2rem;
  /* border: 1px solid red; */
}

.book-3d-img {
  width: 400px;
  animation: orbit 2.4s linear infinite;
}

.chat-3d-img {
  width: 300px;
  animation: orbit 3.8s linear infinite;
  margin-bottom: 4rem;
}

@keyframes orbit {
  0%   { transform: translate(0px, -8px); }
  12.5%{ transform: translate(5.7px, -5.7px); }
  25%  { transform: translate(8px, 0px); }
  37.5%{ transform: translate(5.7px, 5.7px); }
  50%  { transform: translate(0px, 8px); }
  62.5%{ transform: translate(-5.7px, 5.7px); }
  75%  { transform: translate(-8px, 0px); }
  87.5%{ transform: translate(-5.7px, -5.7px); }
  100% { transform: translate(0px, -8px); }
}

.text {
  margin: 3rem;
  font-weight: 600;
}

.ai-test-link {
  text-decoration: none;
  color: #1f2328;
}

.test-link-text {
  background-color: #ffffff;
  border-radius: 10px;
  width: 200px;
  /* height: 40px; */
  margin: 1rem auto;
  padding: 1rem;
  text-align: center;
  font-weight: 800;
  font-size: 18px;
  border: 1px solid #eee;
}

.test-link-text:hover {
  transform: translateY(-2px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.3);
}
</style>
