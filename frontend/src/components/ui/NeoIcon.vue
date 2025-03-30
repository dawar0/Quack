<script setup>
import { computed } from 'vue'
import * as LucideIcons from 'lucide-vue-next'

const props = defineProps({
    name: {
        type: String,
        required: true,
        description: 'The name of the Lucide icon to use (e.g., "check", "x", "circle", etc.)',
    },
    size: {
        type: [Number, String],
        default: 24,
        description: 'Size of the icon in pixels',
    },
    color: {
        type: String,
        default: 'currentColor',
        description: 'Color of the icon',
    },
    strokeWidth: {
        type: [Number, String],
        default: 2,
        description: 'Stroke width of the icon',
    },
    variant: {
        type: String,
        default: '',
        description: 'Visual variant of the icon',
        validator: (value) => ['', 'primary', 'secondary', 'success', 'danger', 'warning', 'info'].includes(value),
    },
    class: {
        type: String,
        default: '',
    }
})

const iconComponent = computed(() => {
    // Convert kebab-case to PascalCase for component name
    const pascalCase = props.name
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('')

    return LucideIcons[pascalCase] || null
})

const variantColor = computed(() => {
    if (!props.variant) return props.color

    const variantMap = {
        primary: '#FF7F50',
        secondary: '#A0A0A0',
        success: '#00FF7F',
        danger: '#FF5555',
        warning: '#FFD700',
        info: '#7FFFD4',
    }

    return variantMap[props.variant] || props.color
})

const iconClasses = computed(() => {
    return [
        'neo-icon',
        props.class,
        props.variant ? `neo-icon-${props.variant}` : '',
    ]
})
</script>

<template>
    <component :is="iconComponent" :size="size" :stroke-width="strokeWidth" :color="variantColor" :class="iconClasses"
        v-if="iconComponent" />
    <span v-else class="neo-icon-missing">
        <!-- Fallback for missing icon -->
        ?
    </span>
</template>

<style scoped>
.neo-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.neo-icon-missing {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: v-bind('`${props.size}px`');
    height: v-bind('`${props.size}px`');
    border: 2px solid currentColor;
    border-radius: 50%;
    font-weight: bold;
}
</style>
