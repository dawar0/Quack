<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: (value) =>
      ['default', 'primary', 'success', 'danger', 'warning', 'info'].includes(value),
  },
  noBorder: {
    type: Boolean,
    default: false,
  },
  noShadow: {
    type: Boolean,
    default: false,
  },
  flat: {
    type: Boolean,
    default: false,
  },
})

const cardClasses = computed(() => {
  return [
    'card',
    'neobrutalism-card',
    `neobrutalism-card-${props.variant}`,
    {
      'no-border': props.noBorder,
      'no-shadow': props.noShadow,
      flat: props.flat,
    },
  ]
})
</script>

<template>
  <div :class="cardClasses">
    <div class="card-header" v-if="$slots.header">
      <slot name="header"></slot>
    </div>
    <div class="card-body">
      <h5 class="card-title" v-if="$slots.title">
        <slot name="title"></slot>
      </h5>
      <h6 class="card-subtitle mb-3 text-muted" v-if="$slots.subtitle">
        <slot name="subtitle"></slot>
      </h6>
      <slot></slot>
    </div>
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<style scoped>
.neobrutalism-card {
  border: 3px solid #000;
  border-radius: 0;
  box-shadow: 8px 8px 0 #000;
  transition: all 0.2s ease;
  overflow: hidden;
  position: relative;
  background-color: #fff;
}

.neobrutalism-card:hover:not(.flat) {
  transform: translate(-3px, -3px);
  box-shadow: 11px 11px 0 #000;
}

.neobrutalism-card-primary {
  background-color: #ff7f50;
}

.neobrutalism-card-success {
  background-color: #00ff7f;
}

.neobrutalism-card-danger {
  background-color: #ff5555;
}

.neobrutalism-card-warning {
  background-color: #ffd700;
}

.neobrutalism-card-info {
  background-color: #7fffd4;
}

.neobrutalism-card .card-header,
.neobrutalism-card .card-footer {
  background-color: rgba(0, 0, 0, 0.05);
  border-bottom: 2px solid #000;
  font-weight: bold;
  padding: 1rem;
}

.neobrutalism-card .card-footer {
  border-top: 2px solid #000;
  border-bottom: none;
}

.neobrutalism-card .card-title {
  font-size: 1.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  position: relative;
}

.neobrutalism-card .card-body {
  padding: 1.5rem;
}

.no-border {
  border: none !important;
}

.no-shadow {
  box-shadow: none !important;
}

.flat:hover {
  transform: none !important;
  box-shadow: 8px 8px 0 #000 !important;
}
</style>
