<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) =>
      ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'].includes(value),
  },
  pill: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
})

const badgeClasses = computed(() => {
  return [
    'badge',
    'neobrutalism-badge',
    `neobrutalism-badge-${props.variant}`,
    `neobrutalism-badge-${props.size}`,
    {
      'rounded-pill': props.pill,
      'rounded-0': !props.pill,
    },
  ]
})
</script>

<template>
  <span :class="badgeClasses">
    <slot></slot>
  </span>
</template>

<style scoped>
.neobrutalism-badge {
  display: inline-block;
  border: 2px solid #000;
  box-shadow: 2px 2px 0 #000;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.2s ease;
  position: relative;
  padding: 0.35em 0.65em;
  margin: 0 2px;
}

.neobrutalism-badge:hover {
  transform: translate(-1px, -1px);
  box-shadow: 3px 3px 0 #000;
}

.neobrutalism-badge-sm {
  font-size: 0.75em;
  border-width: 1px;
  box-shadow: 1px 1px 0 #000;
}

.neobrutalism-badge-sm:hover {
  box-shadow: 2px 2px 0 #000;
}

.neobrutalism-badge-lg {
  font-size: 1em;
  border-width: 3px;
  box-shadow: 3px 3px 0 #000;
  padding: 0.4em 0.75em;
}

.neobrutalism-badge-lg:hover {
  box-shadow: 4px 4px 0 #000;
}

.neobrutalism-badge-primary {
  background-color: #ff7f50;
  color: #000;
}

.neobrutalism-badge-secondary {
  background-color: #a0a0a0;
  color: #000;
}

.neobrutalism-badge-success {
  background-color: #00ff7f;
  color: #000;
}

.neobrutalism-badge-danger {
  background-color: #ff5555;
  color: #000;
}

.neobrutalism-badge-warning {
  background-color: #ffd700;
  color: #000;
}

.neobrutalism-badge-info {
  background-color: #7fffd4;
  color: #000;
}

.neobrutalism-badge-dark {
  background-color: #333;
  color: #fff;
}
</style>
