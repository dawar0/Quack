import { useToast } from 'vue-toastification'

// Get toast instance from Vue Toastification
const toast = useToast()

// Tilting effect function for neo-brutalist style
const getTiltClass = () => {
  const tiltClasses = ['tilt-left', 'tilt-right', 'tilt-none']
  return `Vue-Toastification__toast--${tiltClasses[Math.floor(Math.random() * tiltClasses.length)]}`
}

// Toast service wrapper for Vue Toastification
export const toastService = {
  success(message, options = {}) {
    return toast.success(message, {
      toastClassName: getTiltClass(),
      ...options,
    })
  },

  error(message, options = {}) {
    return toast.error(message, {
      toastClassName: getTiltClass(),
      ...options,
    })
  },

  warning(message, options = {}) {
    return toast.warning(message, {
      toastClassName: getTiltClass(),
      ...options,
    })
  },

  info(message, options = {}) {
    return toast.info(message, {
      toastClassName: getTiltClass(),
      ...options,
    })
  },

  // Raw toast method if needed
  show(message, type = 'default', options = {}) {
    return toast(message, {
      type,
      toastClassName: getTiltClass(),
      ...options,
    })
  },

  // Clear all toasts if needed
  clear() {
    toast.clear()
  },

  // Dismiss a specific toast
  dismiss(id) {
    toast.dismiss(id)
  },
}
