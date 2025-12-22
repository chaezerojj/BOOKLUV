<template>
  <div class="ai-recommend">
    <div class="background-img">
      <div class="ai-main-text">🪄 AI로 취향에 맞는 책과 모임을 찾아드려요!</div>
      <div class="img-box">
        <img class="book-3d-img" src="../../assets/images/3dicons-notebook.png" alt="book-3d-img">
        <img class="chat-3d-img" src="../../assets/images/3dicons-chat.png" alt="chat-3d-img">
      </div>
      <div class="text">⬇️아래 버튼을 눌러 테스트를 시작하세요⬇️</div>
      
      <RouterLink :to="{ name: 'ai-test' }" class="ai-test-link">
        <div class="test-link-text">❤️테스트 하러 가기</div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.ai-recommend {
  /* border: 1px solid red; */
  margin: 0rem auto;
  padding-top: 5rem;
  text-align: center;
  border-radius: 20px;
}

.background-img {
  /* border: 0.1px solid red; */
  margin: 0 auto;
  background-size: 800px;
  background-repeat: no-repeat;
  background-image: url('@/assets/images/tablet2.png');
  background-position: center -1px;
  padding-bottom: 18rem;
}


.ai-main-text {
  font-size: 28px;
  font-weight: 700;
  padding: 2rem;
  padding-top: 12rem;
  margin-top: 1rem;
}

.img-box {
  padding-top: 3rem;
}

.book-3d-img {
  width: 350px;
  animation: orbit 2.4s linear infinite;
}

.chat-3d-img {
  width: 250px;
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
  margin: 2rem;
  margin-top: 5rem;
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
  margin: 1rem auto;
  padding: 1rem;
  text-align: center;
  font-weight: 800;
  font-size: 18px;
  border: 1px solid #e4e4e4;
}

.test-link-text:hover {
  transform: translateY(-2px);
  box-shadow: 2px 2px 12px rgba(161, 161, 161, 0.3);
}
</style>
