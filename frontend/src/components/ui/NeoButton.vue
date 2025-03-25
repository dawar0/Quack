<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'].includes(value),
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  block: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String,
    default: 'button',
  },
  outline: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const handleClick = (event) => {
  emit('click', event)
}

const buttonClasses = computed(() => {
  return [
    'btn',
    `btn-${props.outline ? 'outline-' : ''}${props.variant}`,
    {
      [`btn-${props.size}`]: props.size !== 'md',
      'btn-block w-100': props.block,
      neobrutalism: true,
    },
  ]
})
</script>

<template>
  <button :class="buttonClasses" :type="type" :disabled="disabled" @click="handleClick">
    <slot></slot>
  </button>
</template>

<style scoped>
.neobrutalism {
  border: 3px solid #000;
  border-radius: 0;
  box-shadow: 5px 5px 0 #000;
  font-weight: bold;
  text-transform: uppercase;
  position: relative;
  transition: all 0.2s ease;
  letter-spacing: 0.5px;
}

.neobrutalism:hover:not(:disabled) {
  transform: translate(-2px, -2px);
  box-shadow: 7px 7px 0 #000;
}

.neobrutalism:active:not(:disabled) {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0 #000;
}

.btn-primary.neobrutalism {
  background-color: #ff7f50;
  color: #000;
}

.btn-secondary.neobrutalism {
  background-color: #a0a0a0;
  color: #000;
}

.btn-success.neobrutalism {
  background-color: #00ff7f;
  color: #000;
}

.btn-danger.neobrutalism {
  background-color: #ff5555;
  color: #000;
}

.btn-warning.neobrutalism {
  background-color: #ffd700;
  color: #000;
}

.btn-info.neobrutalism {
  background-color: #7fffd4;
  color: #000;
}

.btn-dark.neobrutalism {
  background-color: #333;
  color: #fff;
}

.btn-outline-primary.neobrutalism {
  background-color: transparent;
  color: #ff7f50;
  box-shadow: 3px 3px 0 #ff7f50;
  border-color: #ff7f50;
}

.btn-outline-secondary.neobrutalism {
  background-color: transparent;
  color: #a0a0a0;
  box-shadow: 3px 3px 0 #a0a0a0;
  border-color: #a0a0a0;
}

.btn-outline-success.neobrutalism {
  background-color: transparent;
  color: #00ff7f;
  box-shadow: 3px 3px 0 #00ff7f;
  border-color: #00ff7f;
}

.btn-outline-danger.neobrutalism {
  background-color: transparent;
  color: #ff5555;
  box-shadow: 3px 3px 0 #ff5555;
  border-color: #ff5555;
}

.btn-outline-warning.neobrutalism {
  background-color: transparent;
  color: #ffd700;
  box-shadow: 3px 3px 0 #ffd700;
  border-color: #ffd700;
}

.btn-outline-info.neobrutalism {
  background-color: transparent;
  color: #7fffd4;
  box-shadow: 3px 3px 0 #7fffd4;
  border-color: #7fffd4;
}

.btn-outline-dark.neobrutalism {
  background-color: transparent;
  color: #333;
  box-shadow: 3px 3px 0 #333;
  border-color: #333;
}

.btn-sm.neobrutalism {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  box-shadow: 3px 3px 0 #000;
}

.btn-lg.neobrutalism {
  padding: 0.5rem 1rem;
  font-size: 1.25rem;
  box-shadow: 8px 8px 0 #000;
}

.btn-lg.neobrutalism:hover:not(:disabled) {
  box-shadow: 10px 10px 0 #000;
}

.btn-lg.neobrutalism:active:not(:disabled) {
  box-shadow: 4px 4px 0 #000;
}

.neobrutalism:disabled {
  opacity: 0.65;
  box-shadow: none;
  cursor: not-allowed;
}
</style>
