<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
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
  rows: {
    type: Number,
    default: 3,
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
    default: () => `textarea-${Math.random().toString(36).substring(2, 11)}`,
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

const textareaClasses = computed(() => {
  return [
    'form-control',
    'neobrutalism-textarea',
    `neobrutalism-textarea-${props.variant}`,
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
    <textarea
      :id="id"
      :class="textareaClasses"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
      :name="name"
      :rows="rows"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
    ></textarea>
    <div v-if="error" class="invalid-feedback neobrutalism-error">
      {{ error }}
    </div>
  </div>
</template>

<style scoped>
.neobrutalism-textarea {
  border: 3px solid #000;
  border-radius: 0;
  background-color: #fff;
  padding: 0.6rem 0.75rem;
  transition: all 0.2s ease;
  font-family: monospace;
  font-size: 1rem;
  resize: vertical;
  min-height: 100px;
}

.neobrutalism-textarea:focus {
  box-shadow: 5px 5px 0 #000;
  transform: translate(-3px, -3px);
  outline: none;
}

.neobrutalism-textarea.is-invalid {
  border-color: #ff5555;
  background-image: none;
}

.neobrutalism-textarea.is-invalid:focus {
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

.neobrutalism-textarea-primary:focus {
  border-color: #ff7f50;
  box-shadow: 5px 5px 0 #ff7f50;
}

.neobrutalism-textarea-success:focus {
  border-color: #00ff7f;
  box-shadow: 5px 5px 0 #00ff7f;
}

.neobrutalism-textarea-danger {
  border-color: #ff5555;
}

.neobrutalism-textarea-danger:focus {
  box-shadow: 5px 5px 0 #ff5555;
}

.neobrutalism-textarea-warning:focus {
  border-color: #ffd700;
  box-shadow: 5px 5px 0 #ffd700;
}

.neobrutalism-textarea-info:focus {
  border-color: #7fffd4;
  box-shadow: 5px 5px 0 #7fffd4;
}

.form-control-sm.neobrutalism-textarea {
  font-size: 0.875rem;
  border-width: 2px;
}

.form-control-sm.neobrutalism-textarea:focus {
  box-shadow: 3px 3px 0 #000;
}

.form-control-lg.neobrutalism-textarea {
  font-size: 1.25rem;
  border-width: 4px;
}

.form-control-lg.neobrutalism-textarea:focus {
  box-shadow: 8px 8px 0 #000;
}
</style>
