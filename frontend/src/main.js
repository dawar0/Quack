import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Toast from 'vue-toastification'
// Import the CSS (or use your own)
import 'vue-toastification/dist/index.css'
// Import our custom neo-brutalist styling (must be after the library CSS)
import './assets/neobrutalist-toast.css'
// Import Lucide icons
import * as LucideIcons from 'lucide-vue-next'

import App from './App.vue'
import router from './router'
import { toastService } from './services/toastService'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

// Register all Lucide icons globally
for (const [key, component] of Object.entries(LucideIcons)) {
  if (key !== 'createLucideIcon') {
    app.component(key, component)
  }
}

// Toast Options
const toastOptions = {
  position: 'bottom-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: true,
  closeButton: 'button',
  icon: true,
  rtl: false,
  maxToasts: 5,
}

app.use(pinia)
app.use(router)
app.use(Toast, toastOptions)

// Add toast service as a global property
app.config.globalProperties.$toast = toastService

app.mount('#app')
