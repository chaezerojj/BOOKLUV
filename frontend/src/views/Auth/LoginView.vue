<template>
  <div class="login">
    <div class="login-text">
      <span>카카오 계정으로</span>
      <span>간편하게 로그인하기</span>
    </div>

    <div class="kakao-btn-box">
      <button class="kakao" type="button" @click="onKakaoLogin">
        <span><img class="talk-img" src="@/assets/images/talk.png" alt="" /></span>
        <span class="kakao-start">카카오로 로그인하기</span>
      </button>
    </div>

    <div class="go-to-signup">
      <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const onKakaoLogin = () => {
  authStore.startKakaoLogin();
};
</script>

<style scoped>
.login {
  display: flex;
  flex-direction: column;
  margin: 5rem auto;
  align-items: center;
  text-align: center;
  border-radius: 16px;
  background-color: #ffffff;
  box-shadow: 0px 0px 50px rgba(0, 0, 0, 0.1);
  width: 350px;
  height: 380px;
}

.login-text {
  display: flex;
  flex-direction: column;
  font-size: 25px;
  font-weight: 700;
  letter-spacing: -0.02rem;
  margin: 4.5rem 3rem;
}

.login-text span {
  margin: 0.3rem;
}

/* ✅ SignupView와 동일 버튼 스타일 */
.kakao {
  width: 180px;
  height: 47px;
  text-align: center;
  background-color: #FEE500;
  border: 0;
  border-radius: 9px;
  cursor: pointer;

  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 0 14px;
}

.talk-img {
  width: 19px;
  display: block;
  margin: 0;
}

.kakao-start {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  white-space: nowrap;
  letter-spacing: -0.02rem;
}

.go-to-signup {
  margin-top: 1rem;
}

.go-to-signup a {
  text-decoration: none;
  color: #7C7C7C;
  font-weight: 500;
  font-size: 13px;
  letter-spacing: -0.04rem;
}
</style>
