<template>
  <div class="kluvtalk-list">
    <!-- todo: swiper로 카드섹션 슬라이드 만들기 -->
    <div class="kluvtalk-maintext">지금 인기있는 KluvTalk!</div>
    <div class="kluvtalk-card-container">
      <div class="kluvtalk-card">
        <img src="https://placehold.co/300x300" alt="">
      </div>
      <div class="kluvtalk-card">
        <img src="https://placehold.co/300x300" alt="">
      </div>
      <div class="kluvtalk-card">
        <img src="https://placehold.co/300x300" alt="">
      </div>
      <div class="kluvtalk-card">
        <img src="https://placehold.co/300x300" alt="">
      </div>
      <div class="kluvtalk-card">
        <img src="https://placehold.co/300x300" alt="">
      </div>
    </div>
    <div class="kluvtalk-create-link-box">
      <RouterLink :to="{name: 'kluvtalk-create'}" class="kluvtalk-create-link">
        <div class="kluvtalk-create-button">
          원하는 KluvTalk이 없나요? 지금 KluvTalk 만들러 가기 ➡️
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


</script>

<style scoped>
.kluvtalk-list {
  border: 1px solid black;
  margin: 1rem auto;
  padding: 0;
  text-align: center;
  width: 100%;
}

.kluvtalk-maintext {
  font-size: 25px;
  font-weight: 800;
  margin-left: 5rem;
}

.kluvtalk-card-container {
  border: 1px solid red;
  display: flex;
  margin: 0 auto;
}

.kluvtalk-create-link-box {
  width: 600px;
  background-color: #ffffff;
  margin: 1rem auto;
  padding: 2rem;
}

.kluvtalk-create-link {
  text-decoration: none;
  color: #1f2328;
  font-size: 20px;
  font-weight: 500;
}

</style>