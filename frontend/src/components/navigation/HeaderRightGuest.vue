<template>
  <div class="header-right-guest">
    <RouterLink :to="{ name: 'login' }" class="link">로그인</RouterLink>
    <RouterLink :to="{ name: 'signup' }" class="link">회원가입</RouterLink>
  </div>
</template>

<script setup></script>

<style scoped>
.header-right-guest {
  width: 150px;
  display: flex;
  justify-content: space-between;
  margin: auto;
  margin-right: 3.5rem;
}

.header-right-guest a {
  text-decoration: none;
  color: #1f2328;
  font-weight: 500;
}

.header-right-guest a:hover {
  font-weight: 700;
}

</style>
