<template>
  <div class="home-card-section">
    <!-- ! 메인 카드섹션 컴포넌트 2개 -->
    <div class="card">카드섹션 1</div>
    <div class="card">카드섹션 2</div>
  </div>
</template>

<script setup>

</script>

<style scoped>
.home-card-section {
  margin: 1rem auto;
  display: flex;
}

.card {
  width: 700px;
  height: 250px;
  margin: 0.2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 2px 2px 8px rgba(161, 161, 161, 0.25);
  text-align: center;
  align-items: center;
  justify-content: center;
}


</style>