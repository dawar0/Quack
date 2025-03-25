<script setup>
import { RouterView } from 'vue-router'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import NeoButton from '@/components/ui/NeoButton.vue'
const router = useRouter()

// In a real application, these would come from an auth store
const isAuthenticated = computed(() => localStorage.getItem('token') !== null)
const userRole = computed(() => localStorage.getItem('role'))

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<template>
  <div class="neo-brutalist">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg bg-black text-white py-2">
      <div class="d-flex justify-content-between w-100 px-4">
        <router-link
          to="/"
          class="navbar-brand fw-semibold bg-white px-2 text-decoration-none"
          style="letter-spacing: -1px; font-size: 1.5rem; border: 4px solid #ff7f50"
        >
          🦆 Quack
        </router-link>
        <button
          class="navbar-toggler border-0"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <i class="bi bi-list text-white" style="font-size: 2rem"></i>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav gap-2">
            <template v-if="!isAuthenticated">
              <li class="nav-item">
                <router-link to="/login" class="nav-link p-0">
                  <NeoButton variant="primary" size="sm" outline>Login</NeoButton>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link p-0">
                  <NeoButton variant="primary" size="sm">Register</NeoButton>
                </router-link>
              </li>
            </template>
            <template v-else>
              <li class="nav-item">
                <a href="#" @click.prevent="logout" class="nav-link p-0">
                  <NeoButton variant="primary" size="sm" outline>Logout</NeoButton>
                </a>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="neo-brutalist">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-black text-white py-4">
      <div class="container text-center">
        <p class="mb-0 fw-bold">&copy; 2024 🦆 Quack. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.neo-brutalist {
  font-family: 'Inter', sans-serif;
  min-height: calc(100vh - 72px - 74px);
}

.navbar {
  border-bottom: 4px solid #ff7f50;
}

.navbar-brand {
  font-size: 1.5rem;
  letter-spacing: 1px;
}

.nav-link {
  display: inline-block;
}

.nav-link.router-link-active .btn {
  background-color: #ff7f50;
  color: #000;
  box-shadow: 3px 3px 0 #000;
}

@media (max-width: 991.98px) {
  .navbar-collapse {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid rgba(255, 255, 255, 0.1);
  }

  .navbar-nav {
    gap: 0.5rem !important;
  }
}
</style>
