import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import './assets/fonts/fonts.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// app.use(createPinia())
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.mount('#app')
