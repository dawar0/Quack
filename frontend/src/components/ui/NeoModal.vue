<script setup>
import { computed, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: '',
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value),
  },
  centered: {
    type: Boolean,
    default: false,
  },
  backdrop: {
    type: Boolean,
    default: true,
  },
  closeOnEscape: {
    type: Boolean,
    default: true,
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) =>
      ['default', 'primary', 'success', 'danger', 'warning', 'info'].includes(value),
  },
  hideCloseButton: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'closed'])

const modalClasses = computed(() => {
  return [
    'modal',
    'fade',
    'neobrutalism-modal',
    {
      show: props.modelValue,
    },
  ]
})

const dialogClasses = computed(() => {
  return [
    'modal-dialog',
    `neobrutalism-modal-${props.variant}`,
    {
      [`modal-${props.size}`]: props.size !== 'md',
      'modal-dialog-centered': props.centered,
    },
  ]
})

const closeModal = () => {
  emit('update:modelValue', false)
  emit('closed')
}

const handleKeyDown = (e) => {
  if (e.key === 'Escape' && props.closeOnEscape && props.modelValue) {
    closeModal()
  }
}

// Add event listener for Escape key
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      document.body.style.overflow = 'hidden'
      document.addEventListener('keydown', handleKeyDown)
    } else {
      document.body.style.overflow = ''
      document.removeEventListener('keydown', handleKeyDown)
    }
  },
)

const handleBackdropClick = (e) => {
  if (e.target.classList.contains('modal') && props.backdrop) {
    closeModal()
  }
}
</script>

<template>
  <div
    v-if="modelValue"
    :class="modalClasses"
    tabindex="-1"
    @click="handleBackdropClick"
    style="display: block"
  >
    <div :class="dialogClasses">
      <div class="modal-content">
        <div class="modal-header" v-if="title || $slots.header">
          <slot name="header">
            <h5 class="modal-title">{{ title }}</h5>
          </slot>
          <button
            v-if="!hideCloseButton"
            type="button"
            class="btn-close"
            @click="closeModal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer" v-if="$slots.footer">
          <slot name="footer"></slot>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="backdrop"></div>
  </div>
</template>

<style scoped>
.neobrutalism-modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.neobrutalism-modal .modal-content {
  border: 3px solid #000;
  border-radius: 0;
  box-shadow: 8px 8px 0 #000;
  overflow: hidden;
  animation: modal-drop 0.3s ease-out forwards;
  transform-origin: top center;
}

@keyframes modal-drop {
  0% {
    transform: translateY(-50px) scale(0.98);
    opacity: 0;
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.neobrutalism-modal .modal-header {
  border-bottom: 2px solid #000;
  padding: 1rem 1.5rem;
}

.neobrutalism-modal .modal-footer {
  border-top: 2px solid #000;
  padding: 1rem 1.5rem;
}
.btn-close {
  border-radius: 0;
}

.neobrutalism-modal .btn-close {
  background: transparent
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M.293.293a1 1 0 011.414 0L8 6.586 14.293.293a1 1 0 111.414 1.414L9.414 8l6.293 6.293a1 1 0 01-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 01-1.414-1.414L6.586 8 .293 1.707a1 1 0 010-1.414z'/%3E%3C/svg%3E")
    center/1em auto no-repeat;
  border: 2px solid #000;
  width: 2rem;
  height: 2rem;
  padding: 0.5rem;
  opacity: 1;
  transition: all 0.2s ease;
}

.neobrutalism-modal .btn-close:hover {
  transform: rotate(90deg);
  background-color: #000;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%23fff' d='M.293.293a1 1 0 011.414 0L8 6.586 14.293.293a1 1 0 111.414 1.414L9.414 8l6.293 6.293a1 1 0 01-1.414 1.414L8 9.414l-6.293 6.293a1 1 0 01-1.414-1.414L6.586 8 .293 1.707a1 1 0 010-1.414z'/%3E%3C/svg%3E");
}

.neobrutalism-modal .modal-title {
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.neobrutalism-modal .modal-body {
  padding: 1.5rem;
}

.neobrutalism-modal-primary .modal-content {
  background-color: #ff7f50;
}

.neobrutalism-modal-success .modal-content {
  background-color: #00ff7f;
}

.neobrutalism-modal-danger .modal-content {
  background-color: #ff5555;
}

.neobrutalism-modal-warning .modal-content {
  background-color: #ffd700;
}

.neobrutalism-modal-info .modal-content {
  background-color: #7fffd4;
}

/* Fix for modal backdrop */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
  width: 100vw;
  height: 100vh;
}
</style>
