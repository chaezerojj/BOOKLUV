<template>
  <div class="ai-test-result">
    <h1>Ai 설문 결과</h1>
    <div class="result-container">
      <div class="result-book-box">
        <img src="https://placehold.co/350x400" alt="">
        <div class="result-book-detail">
          책 상세 페이지로 이동 (링크 달기)
        </div>
      </div>
      <div class="result-kluvtalk-box">
        <h3>추천된 책으로 개설된 kluvtalk은 00개 입니다.</h3>
        <div class="result-kluvtalk-list">
          개설된 모임들 리스트 페이지로 이동 (링크 달기)
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>

</script>


<style scoped>
.ai-test-result {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 2rem;
  text-align: center;
}

.result-container {
  border: 1px solid black;
  max-width: 1000px;
  display: flex;
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
  justify-content: space-around;
}

</style>