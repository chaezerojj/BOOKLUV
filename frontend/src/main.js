import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

import "./assets/fonts/fonts.css";

import App from "./App.vue";
import router from "./router";

import { http } from "@/api/http";
import { useAuthStore } from "@/stores/auth";

async function bootstrap() {
  const app = createApp(App);

  // Pinia 세팅
  const pinia = createPinia();
  pinia.use(piniaPluginPersistedstate);
  app.use(pinia);

  // Router 세팅
  app.use(router);

  // CSRF 쿠키 심기 (세션쿠키/CSRF 쓰는 경우)
  try {
    await http.get("/api/v1/auth/csrf/");
  } catch (e) {
    console.warn("CSRF cookie init failed:", e);
  }

  // 로그인 상태 복구(세션 기반이면 fetchMe로 서버에 확인)
  try {
    const authStore = useAuthStore(pinia);
    await authStore.fetchMe();
  } catch (e) {
    console.warn("fetchMe failed:", e);
  }

  // mount는 딱 1번만
  app.mount("#app");
}

bootstrap();
