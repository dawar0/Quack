<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value),
  },
  dismissible: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
  icon: {
    type: String,
    default: '',
  },
})

const visible = ref(true)

const closeAlert = () => {
  visible.value = false
}

const alertClasses = computed(() => {
  return [
    'alert',
    'neobrutalism-alert',
    `neobrutalism-alert-${props.variant}`,
    {
      'alert-dismissible': props.dismissible,
    },
  ]
})

const backgroundClasses = computed(() => {
  const variantMap = {
    primary: '#FF7F50',
    secondary: '#A0A0A0',
    success: '#00FF7F',
    danger: '#FF5555',
    warning: '#FFD700',
    info: '#7FFFD4',
  }

  return variantMap[props.variant] || '#FF7F50'
})

const iconClasses = computed(() => {
  if (!props.icon) return ''

  return `bi bi-${props.icon} alert-icon`
})
</script>

<template>
  <div
    v-if="visible"
    :class="alertClasses"
    role="alert"
    :style="{ backgroundColor: backgroundClasses }"
  >
    <div class="d-flex">
      <div v-if="icon" class="alert-icon-wrapper me-3">
        <i :class="iconClasses"></i>
      </div>
      <div>
        <h5 v-if="title" class="alert-heading">{{ title }}</h5>
        <slot></slot>
      </div>
    </div>
    <button
      v-if="dismissible"
      type="button"
      class="btn-close"
      @click="closeAlert"
      aria-label="Close"
    ></button>
  </div>
</template>

<style scoped>
.neobrutalism-alert {
  border: 3px solid #000;
  border-radius: 0;
  box-shadow: 5px 5px 0 #000;
  transition: all 0.2s ease;
  color: #000;
  padding: 1rem;
  position: relative;
  font-weight: 500;
}

.neobrutalism-alert:hover {
  transform: translate(-2px, -2px);
  box-shadow: 7px 7px 0 #000;
}

.neobrutalism-alert .alert-heading {
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.alert-icon-wrapper {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  font-size: 1.25rem;
}

.btn-close {
  background: transparent
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M.293.293a1 1 0 011.414 0L8 6.586 14.293.293a1 1 0 111.414 1.414L9.414 8l6.293 6.293a1 1 0 01-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 01-1.414-1.414L6.586 8 .293 1.707a1 1 0 010-1.414z'/%3E%3C/svg%3E")
    center/1em auto no-repeat;
  border: 2px solid #000;
  width: 2rem;
  height: 2rem;
  padding: 0.5rem;
  opacity: 1;
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  transition: all 0.2s ease;
}

.btn-close:hover {
  transform: rotate(90deg);
  background-color: #000;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%23fff' d='M.293.293a1 1 0 011.414 0L8 6.586 14.293.293a1 1 0 111.414 1.414L9.414 8l6.293 6.293a1 1 0 01-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 01-1.414-1.414L6.586 8 .293 1.707a1 1 0 010-1.414z'/%3E%3C/svg%3E");
}

.alert-dismissible {
  padding-right: 3.5rem;
}
</style>
