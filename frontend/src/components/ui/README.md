# Neo-Brutalist UI Components

A collection of Vue 3 components with a Neo-Brutalist design style for your Bootstrap-based projects. These components are built with a shadcn-like architecture for easy importing and usage.

## Installation

These components are already included in your project. Use them directly by importing from the UI components directory.

```js
import { NeoButton, NeoCard } from '@/components/ui'
```

## Components

### NeoButton

A Neo-Brutalist styled button component.

```vue
<template>
  <NeoButton>Default Button</NeoButton>
  <NeoButton variant="success">Success Button</NeoButton>
  <NeoButton variant="danger" size="lg">Large Danger Button</NeoButton>
  <NeoButton variant="primary" outline>Outline Button</NeoButton>
  <NeoButton disabled>Disabled Button</NeoButton>
  <NeoButton block>Block Button</NeoButton>
</template>

<script setup>
import { NeoButton } from '@/components/ui'
</script>
```

**Props:**

- `variant`: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'dark' (default: 'primary')
- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `disabled`: boolean (default: false)
- `block`: boolean (default: false)
- `type`: string (default: 'button')
- `outline`: boolean (default: false)

### NeoCard

A Neo-Brutalist styled card component.

```vue
<template>
  <NeoCard>
    <template #title>Card Title</template>
    <template #subtitle>Card Subtitle</template>
    <p>This is the card content.</p>
    <template #footer>Card Footer</template>
  </NeoCard>

  <NeoCard variant="primary">
    <template #header>Card Header</template>
    <p>This is a primary card.</p>
  </NeoCard>
</template>

<script setup>
import { NeoCard } from '@/components/ui'
</script>
```

**Props:**

- `variant`: 'default' | 'primary' | 'success' | 'danger' | 'warning' | 'info' (default: 'default')
- `noBorder`: boolean (default: false)
- `noShadow`: boolean (default: false)
- `flat`: boolean (default: false)

**Slots:**

- `default`: Main content
- `header`: Card header
- `title`: Card title
- `subtitle`: Card subtitle
- `footer`: Card footer

### NeoInput

A Neo-Brutalist styled input component.

```vue
<template>
  <NeoInput v-model="inputValue" label="Username" placeholder="Enter username" required />

  <NeoInput v-model="password" type="password" label="Password" error="Password is required" />
</template>

<script setup>
import { ref } from 'vue'
import { NeoInput } from '@/components/ui'

const inputValue = ref('')
const password = ref('')
</script>
```

**Props:**

- `modelValue`: string | number (default: '')
- `label`: string (default: '')
- `placeholder`: string (default: '')
- `type`: string (default: 'text')
- `required`: boolean (default: false)
- `disabled`: boolean (default: false)
- `readonly`: boolean (default: false)
- `id`: string (default: auto-generated)
- `name`: string (default: '')
- `error`: string (default: '')
- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `variant`: 'default' | 'primary' | 'success' | 'danger' | 'warning' | 'info' (default: 'default')

### NeoSelect

A Neo-Brutalist styled select component.

```vue
<template>
  <NeoSelect v-model="selectedValue" :options="options" label="Choose an option" required />

  <NeoSelect v-model="multiSelectedValues" :options="options" label="Select multiple" multiple />
</template>

<script setup>
import { ref } from 'vue'
import { NeoSelect } from '@/components/ui'

const selectedValue = ref('')
const multiSelectedValues = ref([])
const options = [
  { value: 'option1', label: 'Option 1' },
  { value: 'option2', label: 'Option 2' },
  { value: 'option3', label: 'Option 3', disabled: true },
]
</script>
```

**Props:**

- `modelValue`: string | number | array (default: '')
- `options`: array of { value, label, disabled? } objects (required)
- `label`: string (default: '')
- `placeholder`: string (default: 'Select an option')
- `required`: boolean (default: false)
- `disabled`: boolean (default: false)
- `multiple`: boolean (default: false)
- `id`: string (default: auto-generated)
- `name`: string (default: '')
- `error`: string (default: '')
- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `variant`: 'default' | 'primary' | 'success' | 'danger' | 'warning' | 'info' (default: 'default')

### NeoAlert

A Neo-Brutalist styled alert component.

```vue
<template>
  <NeoAlert variant="success" title="Success" icon="check-circle">
    Operation completed successfully!
  </NeoAlert>

  <NeoAlert variant="danger" dismissible> Something went wrong. Please try again. </NeoAlert>
</template>

<script setup>
import { NeoAlert } from '@/components/ui'
</script>
```

**Props:**

- `variant`: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' (default: 'primary')
- `dismissible`: boolean (default: false)
- `title`: string (default: '')
- `icon`: string (default: '') - Bootstrap icon name

### NeoBadge

A Neo-Brutalist styled badge component.

```vue
<template>
  <NeoBadge>Default</NeoBadge>
  <NeoBadge variant="success">Success</NeoBadge>
  <NeoBadge variant="danger" size="lg">Error</NeoBadge>
  <NeoBadge variant="warning" pill>Warning</NeoBadge>
</template>

<script setup>
import { NeoBadge } from '@/components/ui'
</script>
```

**Props:**

- `variant`: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info' | 'dark' (default: 'primary')
- `pill`: boolean (default: false)
- `size`: 'sm' | 'md' | 'lg' (default: 'md')

### NeoModal

A Neo-Brutalist styled modal dialog component.

```vue
<template>
  <NeoButton @click="showModal = true">Open Modal</NeoButton>

  <NeoModal v-model="showModal" title="Modal Title" variant="primary" centered>
    <p>This is the modal content.</p>

    <template #footer>
      <NeoButton variant="danger" @click="showModal = false">Close</NeoButton>
      <NeoButton variant="success">Save Changes</NeoButton>
    </template>
  </NeoModal>
</template>

<script setup>
import { ref } from 'vue'
import { NeoButton, NeoModal } from '@/components/ui'

const showModal = ref(false)
</script>
```

**Props:**

- `modelValue`: boolean (default: false) - Controls the visibility of the modal
- `title`: string (default: '')
- `size`: 'sm' | 'md' | 'lg' | 'xl' (default: 'md')
- `centered`: boolean (default: false) - Centers the modal vertically
- `backdrop`: boolean (default: true) - Enables click outside to close
- `closeOnEscape`: boolean (default: true) - Enables escape key to close
- `variant`: 'default' | 'primary' | 'success' | 'danger' | 'warning' | 'info' (default: 'default')
- `hideCloseButton`: boolean (default: false)

**Slots:**

- `default`: Modal body content
- `header`: Custom header (replaces title)
- `footer`: Modal footer content

**Events:**

- `update:modelValue`: Emitted when modal opens or closes
- `closed`: Emitted when modal closes

## NeoIcon

A component that makes it easy to use Lucide icons in your app.

### Usage

```vue
<template>
  <!-- Basic usage -->
  <NeoIcon name="check" />
  
  <!-- With custom size and color -->
  <NeoIcon name="alert-circle" size="32" color="red" />
  
  <!-- With predefined color variants -->
  <NeoIcon name="info" variant="info" />
  
  <!-- With custom stroke width -->
  <NeoIcon name="star" stroke-width="1.5" />
</template>
```

### Props

| Prop        | Type             | Default        | Description                        |
|-------------|------------------|----------------|------------------------------------|
| name        | String           | (required)     | Name of the Lucide icon to use     |
| size        | Number or String | 24             | Size of the icon in pixels         |
| color       | String           | 'currentColor' | Color of the icon                  |
| strokeWidth | Number or String | 2              | Stroke width of the icon           |
| variant     | String           | ''             | Color variant (primary, success, etc) |
| class       | String           | ''             | Additional CSS classes to apply    |

### Available Icons

All icons from the Lucide icon library are available. You can find the complete list of icons at [https://lucide.dev/icons/](https://lucide.dev/icons/).

When using an icon, convert the icon name to kebab-case. For example:
- `AlertTriangle` → `alert-triangle`
- `CheckCircle` → `check-circle`
- `ChevronRight` → `chevron-right`

## Customization

These components use Bootstrap's classes with custom Neo-Brutalist styling. You can further customize these components by modifying their styles or extending them with your own modifications.
