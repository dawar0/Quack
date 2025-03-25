<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  readonly: {
    type: Boolean,
    default: false,
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substring(2, 11)}`,
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

const emit = defineEmits(['update:modelValue', 'focus', 'blur', 'input'])

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
  emit('input', event)
}

const handleFocus = (event) => {
  emit('focus', event)
}

const handleBlur = (event) => {
  emit('blur', event)
}

const inputClasses = computed(() => {
  return [
    'form-control',
    'neobrutalism-input',
    `neobrutalism-input-${props.variant}`,
    {
      [`form-control-${props.size}`]: props.size !== 'md',
      'is-invalid': props.error,
    },
  ]
})

const inputGroupClasses = computed(() => {
  return [
    'mb-3',
    {
      'has-validation': props.error,
    },
  ]
})
</script>

<template>
  <div :class="inputGroupClasses">
    <label v-if="label" :for="id" class="form-label neobrutalism-label">
      {{ label }}
      <span v-if="required" class="text-danger">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :class="inputClasses"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
      :name="name"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
    />
    <div v-if="error" class="invalid-feedback neobrutalism-error">
      {{ error }}
    </div>
  </div>
</template>

<style scoped>
.neobrutalism-input {
  border: 3px solid #000;
  border-radius: 0;
  background-color: #fff;
  padding: 0.6rem 0.75rem;
  transition: all 0.2s ease;
  font-family: monospace;
  font-size: 1rem;
}

.neobrutalism-input:focus {
  box-shadow: 5px 5px 0 #000;
  transform: translate(-3px, -3px);
  outline: none;
}

.neobrutalism-input.is-invalid {
  border-color: #ff5555;
  background-image: none;
}

.neobrutalism-input.is-invalid:focus {
  box-shadow: 5px 5px 0 #ff5555;
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

.neobrutalism-input-primary:focus {
  border-color: #ff7f50;
  box-shadow: 5px 5px 0 #ff7f50;
}

.neobrutalism-input-success:focus {
  border-color: #00ff7f;
  box-shadow: 5px 5px 0 #00ff7f;
}

.neobrutalism-input-danger {
  border-color: #ff5555;
}

.neobrutalism-input-danger:focus {
  box-shadow: 5px 5px 0 #ff5555;
}

.neobrutalism-input-warning:focus {
  border-color: #ffd700;
  box-shadow: 5px 5px 0 #ffd700;
}

.neobrutalism-input-info:focus {
  border-color: #7fffd4;
  box-shadow: 5px 5px 0 #7fffd4;
}

.form-control-sm.neobrutalism-input {
  font-size: 0.875rem;
  border-width: 2px;
}

.form-control-sm.neobrutalism-input:focus {
  box-shadow: 3px 3px 0 #000;
}

.form-control-lg.neobrutalism-input {
  font-size: 1.25rem;
  border-width: 4px;
}

.form-control-lg.neobrutalism-input:focus {
  box-shadow: 8px 8px 0 #000;
}
</style>
