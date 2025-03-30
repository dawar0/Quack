<script setup>
const props = defineProps({
    modelValue: {
        type: [String, Number],
        required: true,
    },
    tabs: {
        type: Array,
        required: true,
        validator: (value) => {
            return value.every((tab) => typeof tab.value !== 'undefined' && typeof tab.label !== 'undefined')
        }
    },
    variant: {
        type: String,
        default: 'primary',
        validator: (value) =>
            ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'dark'].includes(value),
    },
})

const emit = defineEmits(['update:modelValue'])

const updateActiveTab = (value) => {
    emit('update:modelValue', value)
}

const isActive = (tabValue) => {
    return props.modelValue === tabValue
}
</script>

<template>
    <div class="neobrutalism-tabs-wrapper">
        <ul class="neobrutalism-tabs" :class="`neobrutalism-tabs-${variant}`">
            <li v-for="tab in tabs" :key="tab.value" class="neobrutalism-tab-item">
                <button type="button" class="neobrutalism-tab-button" :class="{ 'active': isActive(tab.value) }"
                    @click="updateActiveTab(tab.value)">
                    {{ tab.label }}
                </button>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.neobrutalism-tabs-wrapper {
    margin-bottom: 1.5rem;
    display: block;
    position: relative;
}

.neobrutalism-tabs {
    list-style: none;
    display: flex;
    padding: 0;
    margin: 0;
    gap: 10px;
    border-bottom: 3px solid #000;
}

.neobrutalism-tab-item {
    margin-bottom: -3px;
}

.neobrutalism-tab-button {
    border: 3px solid #000;
    border-bottom: 0;
    background-color: #f0f0f0;
    color: #000;
    padding: 0.75rem 1.5rem;
    font-weight: bold;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    margin-bottom: -3px;
    outline: none;
    letter-spacing: 0.5px;
}

.neobrutalism-tab-button:hover:not(.active) {
    transform: translateY(-3px);
    border-top-color: #000;
}

.neobrutalism-tab-button.active {
    border-bottom: 3px solid #fff;
    margin-bottom: -3px;
    z-index: 1;
    transform: translateY(-5px);
    box-shadow: 5px -3px 0 #000;
}

/* Variants */
.neobrutalism-tabs-primary .neobrutalism-tab-button.active {
    background-color: #ff7f50;
}

.neobrutalism-tabs-secondary .neobrutalism-tab-button.active {
    background-color: #a0a0a0;
}

.neobrutalism-tabs-success .neobrutalism-tab-button.active {
    background-color: #00ff7f;
}

.neobrutalism-tabs-danger .neobrutalism-tab-button.active {
    background-color: #ff5555;
}

.neobrutalism-tabs-warning .neobrutalism-tab-button.active {
    background-color: #ffd700;
}

.neobrutalism-tabs-info .neobrutalism-tab-button.active {
    background-color: #7fffd4;
}

.neobrutalism-tabs-dark .neobrutalism-tab-button.active {
    background-color: #333;
    color: #fff;
}
</style>
