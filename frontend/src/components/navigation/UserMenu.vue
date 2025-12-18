<template>
  <div class="user-menu" ref="root">
    <button class="menu-toggle" type="button" @mousedown.prevent="toggle" :aria-expanded="open" aria-haspopup="menu">
      <img src="@/assets/images/account_circle.png" alt="user-account-img" class="account-img">
    </button>

    <div class="menu" :class="{ open }" role="menu">
      <RouterLink :to="{name: 'mypage-info'}" class="item">마이페이지</RouterLink>
      <RouterLink :to="{name: 'mypage-mykluv'}" class="item">나의 모임</RouterLink>
      <button class="item" type="button" @mousedown.prevent="onLogout">로그아웃</button>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const root = ref(null)
const open = ref(false)

const toggle = () => { open.value = !open.value }
const close = () => { open.value = false }

const onClickOutside = (e) => {
  if (!root.value) return
  if (!root.value.contains(e.target)) close()
}

const onLogout = () => {
  // TODO: 토큰/유저 상태 초기화
  close()
  router.push('/')
}

onMounted(() => document.addEventListener('mousedown', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('mousedown', onClickOutside))

</script>


<style scoped>
.user-menu {
  position: relative;
  display: flex;
  margin: 0;
}

.account-img {
  width: 25px;
  margin: 0;
  padding: 0;
}

button {
  cursor: pointer;
  border: none;
  outline: none;
  background-color: inherit;
}

/* 드롭다운탭 (기본: 닫혀있음) */
.menu {
  border: 0.5px solid rgba(161, 161, 161, 0.25);
  background-color: #ffffff;
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  min-width: 100px;
  height: 120px;
  border-radius: 10px;
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-1px);
  pointer-events: none;
  transition: opacity .15s ease, transform .15s ease, visibility .1s;
}

.menu.open {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
  pointer-events: auto;
}

.item {
  width: 100%;
  height: 40px;
  font-size: 15px;
  color: #1f2328;
  display: block;
  text-decoration: none;
  font-weight: 500;
  text-align: center;
  padding: 0;
  border-radius: 10px;
}

.item:hover {
  font-weight: 700;
  background-color: rgba(161, 161, 161, 0.1);
}

</style>