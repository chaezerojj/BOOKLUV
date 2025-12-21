<template>
  <div class="home-hero-section">
    <!-- ! 대문 이미지 -->
    <div class="img-box">
      <img src="../../assets/images/book_and_cup.png" alt="book-and-cup-img" class="book-and-cup-img">
    </div>
    <div class="main-text-box">
      <span class="main-text">지금 유저들은 어떤 책으로 대화를 나누고 있을까요?</span>
      <RouterLink :to="{name: 'kluvtalk-list'}" class="kluvtalk-btn-link">알아보러가기 <span class="right">➡️</span></RouterLink>
    </div>
  </div>
</template>


<script setup>
import { RouterLink } from 'vue-router';


</script>


<style scoped>
.home-hero-section {
  margin: 1rem auto;
  /* background-color: #fff; */
  border-radius: 15px;
  /* box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25); */
  height: 250px;
  display: flex;
  padding: 2rem;
  /* justify-content: space-around; */
  text-align: center;
  align-items: center;
}

.img-box {
  margin: 4rem;
  padding: 0;
  /* border: 1px solid red; */
}

.book-and-cup-img {
  width: 300px;
}

.main-text-box {
  display: flex;
  flex-direction: column;
  align-items: end;
  justify-content: flex-end;
  margin: 4rem;
  margin-left: 7rem;
}

.main-text {
  font-size: 25px;
  font-weight: 400;
  margin: 1rem;
}

.kluvtalk-btn-link {
  width: 150px;
  height: 40px;
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 400;
  font-size: 20px;
  margin-top: 1rem;
  /* margin: 1rem; */
  /* background-color: #82adff; */
  color: #1f2328;
}

.kluvtalk-btn-link:hover {
  color: #1f2328;
  transform: translateX(4px);
  /* box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25); */
}

</style>