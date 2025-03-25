<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Array],
    default: '',
  },
  options: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(
        (option) => typeof option === 'object' && 'value' in option && 'label' in option,
      )
    },
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Select an option',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  id: {
    type: String,
    default: () => `select-${Math.random().toString(36).substring(2, 11)}`,
  },
  name: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) =>
      ['default', 'primary', 'success', 'danger', 'warning', 'info'].includes(value),
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const handleInput = (event) => {
  let value
  if (props.multiple) {
    const options = Array.from(event.target.selectedOptions)
    value = options.map((option) => option.value)
  } else {
    value = event.target.value
  }
  emit('update:modelValue', value)
  emit('change', event)
}

const selectClasses = computed(() => {
  return [
    'form-select',
    'neobrutalism-select',
    `neobrutalism-select-${props.variant}`,
    {
      [`form-select-${props.size}`]: props.size !== 'md',
      'is-invalid': props.error,
    },
  ]
})

const formGroupClasses = computed(() => {
  return [
    'mb-3',
    {
      'has-validation': props.error,
    },
  ]
})
</script>

<template>
  <div :class="formGroupClasses">
    <label v-if="label" :for="id" class="form-label neobrutalism-label">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    <select
      :id="id"
      :class="selectClasses"
      :value="modelValue"
      :required="required"
      :disabled="disabled"
      :name="name"
      :multiple="multiple"
      @input="handleInput"
    >
      <option v-if="!multiple && !required" value="" disabled selected hidden>
        {{ placeholder }}
      </option>
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
        :disabled="option.disabled"
      >
        {{ option.label }}
      </option>
    </select>
    <div v-if="error" class="invalid-feedback neobrutalism-error">
      {{ error }}
    </div>
  </div>
</template>

<style scoped>
.neobrutalism-select {
  border: 3px solid #000;
  border-radius: 0;
  background-color: #fff;
  padding: 0.6rem 2rem 0.6rem 0.75rem;
  transition: all 0.2s ease;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%23000000' stroke-linecap='round' stroke-linejoin='round' stroke-width='3' d='M2 5l6 6 6-6'/%3E%3C/svg%3E");
  background-position: right 0.75rem center;
  background-size: 16px 12px;
  font-family: monospace;
  font-size: 1rem;
  font-weight: bold;
}

.neobrutalism-select:focus {
  box-shadow: 5px 5px 0 #000;
  transform: translate(-3px, -3px);
  outline: none;
}

.neobrutalism-select.is-invalid {
  border-color: #ff5555;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3E%3Cpath fill='none' stroke='%23FF5555' stroke-linecap='round' stroke-linejoin='round' stroke-width='3' d='M2 5l6 6 6-6'/%3E%3C/svg%3E");
}

.neobrutalism-select.is-invalid:focus {
  box-shadow: 5px 5px 0 #ff5555;
}

.neobrutalism-select[multiple] {
  background-image: none;
  padding-right: 0.75rem;
}

.neobrutalism-label {
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.neobrutalism-error {
  font-weight: bold;
  font-size: 0.8rem;
}

.neobrutalism-select-primary:focus {
  border-color: #ff7f50;
  box-shadow: 5px 5px 0 #ff7f50;
}

.neobrutalism-select-success:focus {
  border-color: #00ff7f;
  box-shadow: 5px 5px 0 #00ff7f;
}

.neobrutalism-select-danger {
  border-color: #ff5555;
}

.neobrutalism-select-danger:focus {
  box-shadow: 5px 5px 0 #ff5555;
}

.neobrutalism-select-warning:focus {
  border-color: #ffd700;
  box-shadow: 5px 5px 0 #ffd700;
}

.neobrutalism-select-info:focus {
  border-color: #7fffd4;
  box-shadow: 5px 5px 0 #7fffd4;
}

.form-select-sm.neobrutalism-select {
  font-size: 0.875rem;
  border-width: 2px;
  padding: 0.35rem 1.75rem 0.35rem 0.5rem;
}

.form-select-sm.neobrutalism-select:focus {
  box-shadow: 3px 3px 0 #000;
}

.form-select-lg.neobrutalism-select {
  font-size: 1.25rem;
  border-width: 4px;
  padding: 0.75rem 2.25rem 0.75rem 0.75rem;
}

.form-select-lg.neobrutalism-select:focus {
  box-shadow: 8px 8px 0 #000;
}
</style>
