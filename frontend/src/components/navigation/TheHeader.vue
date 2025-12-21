<template>
  <div class="header-container">
    <div class="header">
      <RouterLink :to="{name: 'home'}">
        <img class="logo" src="@/assets/images/BOOKLUV_LOGO.png" alt="main-logo">
      </RouterLink>
      <!-- <h1>네비바 전체 list</h1> -->
      <!-- 카테고리 -->
      <HeaderNav /> 
      <HeaderRight />
    </div>
  </div>
</template>

<script setup>
import HeaderNav from './HeaderNav.vue';
import HeaderRight from './HeaderRight.vue';


</script>

<style scoped>
.header-container {
  width: 100%;
  top: 0;
  margin: 0;
  padding: 0;
  text-align: justify;
  padding-top: 40px;
  font-size: 17px;
  letter-spacing: -0.05rem;
}

.header {
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: inset -5px -5px 9px rgba(161, 161, 161, 0.25);
  display: flex;
  width: 1300px;
  height: 90px;
  align-items: center;
  justify-content: space-between;
  margin: auto;
}

.logo {
  width: 135px;
  margin: 1.5rem;
  margin-left: 4rem;
}

</style>