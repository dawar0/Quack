import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Toast from 'vue-toastification'
// Import the CSS (or use your own)
import 'vue-toastification/dist/index.css'
// Import our custom neo-brutalist styling (must be after the library CSS)
import './assets/neobrutalist-toast.css'

import App from './App.vue'
import router from './router'
import { toastService } from './services/toastService'

const app = createApp(App)

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

app.use(createPinia())
app.use(router)
app.use(Toast, toastOptions)

// Add toast service as a global property
app.config.globalProperties.$toast = toastService

app.mount('#app')
