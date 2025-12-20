<template>
  <div class="container">
    <!-- <h1>네비바 전체 list</h1> -->
    <!-- 카테고리 -->
    <HeaderNav /> 
    <HeaderRight />
  </div>
</template>

<script setup>
import HeaderNav from './HeaderNav.vue';
import HeaderRight from './HeaderRight.vue';


</script>

<style scoped>
.container {
  border: 1px solid red;
  display: flex;
}

.container div {
  border: 1px solid blue;
}
</style>