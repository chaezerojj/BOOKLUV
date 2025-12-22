import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/fonts/fonts.css'

import App from './App.vue'
import router from './router'

import { useAuthStore } from "@/stores/auth";

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

// ✅ 앱 시작 시 세션 로그인 여부 확인
const authStore = useAuthStore();
authStore.fetchMe();

app.mount('#app')
