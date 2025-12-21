<template>
  <div class="ai-test">
    AI 취향 설문조사 페이지
    <div class="test-container">
      <ul class="test-question">질문태그
        <li class="answer">선지1</li>
        <li class="answer">선지2</li>
        <li class="answer">선지3</li>
        <li class="answer">선지4</li>
      </ul>
      <ul class="test-question">질문태그
        <li class="answer">선지1</li>
        <li class="answer">선지2</li>
        <li class="answer">선지3</li>
        <li class="answer">선지4</li>
      </ul>
      <ul class="test-question">질문태그
        <li class="answer">선지1</li>
        <li class="answer">선지2</li>
        <li class="answer">선지3</li>
        <li class="answer">선지4</li>
      </ul>
      <ul class="test-question">질문태그
        <li class="answer">선지1</li>
        <li class="answer">선지2</li>
        <li class="answer">선지3</li>
        <li class="answer">선지4</li>
      </ul>
    </div>
    <RouterLink :to="{name: 'ai-result'}" class="ai-result-link">
      <div class="ai-result-text">🤖 테스트 결과 보러가기</div>
    </RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


</script>

<style scoped>
.ai-test {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.test-container {
  width: 800px;
  margin: 0 auto;
}

.test-question {
  border: 1px solid red;
  list-style-type: none;
  font-size: 20px;
}

.ai-result-link {
  text-decoration: none;
  color: #1f2328;
}

.ai-result-text:hover {
  transform: translateY(-2px);
  box-shadow: 2px 2px 1 rgba(161, 161, 161, 0.3);
}

.ai-result-text {
  background-color: #ffffff;
  border: 0.5px solid rgba(161, 161, 161, 0.25);
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


</style>