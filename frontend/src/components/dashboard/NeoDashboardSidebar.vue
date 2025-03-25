<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

// Use destructuring to make it clear props are being used
const { menuItems, title } = defineProps({
  menuItems: {
    type: Array,
    required: true,
  },
  theme: {
    type: String,
    default: 'light', // 'light' or 'dark'
    validator: (value) => ['light', 'dark'].includes(value),
  },
  title: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['item-action'])

const router = useRouter()
const currentRoute = computed(() => router.currentRoute.value.path)
const currentRouteName = computed(() => router.currentRoute.value.name)

// Determine if a menu item is active
const isActive = (item) => {
  if (item.exactPath) {
    return currentRoute.value === item.route
  }

  if (item.routeName) {
    return currentRouteName.value === item.routeName
  }

  return currentRoute.value.includes(item.route)
}

// Handle menu item click
const handleItemClick = (item) => {
  if (item.action) {
    emit('item-action', item)
    return
  }
}
</script>

<template>
  <div class="neo-sidebar">
    <div class="pt-3">
      <div v-if="title" class="sidebar-title">{{ title }}</div>
      <ul class="nav flex-column">
        <li v-for="item in menuItems" :key="item.route" class="nav-item">
          <router-link
            v-if="!item.action"
            :to="item.route"
            class="nav-link"
            :class="{ active: isActive(item) }"
          >
            <i v-if="item.icon" :class="item.icon + ' me-2'"></i>
            <span>{{ item.label }}</span>
          </router-link>
          <a
            v-else
            href="#"
            @click.prevent="handleItemClick(item)"
            class="nav-link"
            :class="{ 'text-danger': item.label === 'Logout' }"
          >
            <i v-if="item.icon" :class="item.icon + ' me-2'"></i>
            <span>{{ item.label }}</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.neo-sidebar {
  background-color: #ffffff;
  font-family: 'Inter', sans-serif;
  width: 100%;
}

.sidebar-title {
  padding: 0 28px 10px;
  font-weight: 900;
  font-size: 1.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #000;
  border-bottom: 4px solid #ff7f50;
}

.nav-item {
  transition: all 0.2s ease;
  margin: 2px 0px 2px 0;
}

.nav-link {
  font-weight: 700;
  color: #333;

  padding: 5px 20px;
  margin: 4px 0;
  transition: all 0.2s ease;
  letter-spacing: 0.5px;
  font-size: 1.2rem;
  border: 2px solid transparent;
  display: block;
  text-decoration: none;
}

.nav-link:hover {
  background-color: rgba(255, 127, 80, 0.1);
  transform: translateX(4px);
}

.nav-link.active {
  color: #000;
  background-color: #ff7f50;
  box-shadow: 3px 3px 0 #000;
  transform: translateY(-2px);
  border: 2px solid #000;
  border-radius: 0;
  margin-right: 8px;
}

@media (max-width: 767.98px) {
  .neo-sidebar {
    position: static;
    padding-top: 0;
    border-right: none;
    border-bottom: 4px solid #000;
    margin-bottom: 20px;
  }

  .nav-link.active {
    box-shadow: 2px 2px 0 #000;
  }
}
</style>
