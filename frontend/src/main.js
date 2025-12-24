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

app.use(pinia);
const authStore = useAuthStore(pinia); // pinia 인스턴스 명시
await authStore.fetchMe();
app.use(router);
app.mount("#app");