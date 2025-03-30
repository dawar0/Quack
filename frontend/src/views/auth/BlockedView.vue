<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { NeoButton, NeoIcon } from '@/components/ui'

const authStore = useAuthStore()
const router = useRouter()

const logout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="blocked-container text-center">
    <div class="blocked-card">
      <NeoIcon name="ban" size="64" class="text-danger mb-4" />
      <h1>Account Blocked</h1>
      <p class="lead">Your account has been blocked.</p>
      <p>Please contact our admin team for further assistance.</p>

      <div class="action-buttons mt-4">
        <NeoButton variant="secondary" @click="logout">Logout</NeoButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.blocked-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.blocked-card {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  border: 4px solid #000;
  background: white;
  box-shadow: 8px 8px 0 #000;
}

h1 {
  font-weight: 900;
  margin-bottom: 1rem;
}

.text-danger {
  color: #ff5555;
}
</style>
