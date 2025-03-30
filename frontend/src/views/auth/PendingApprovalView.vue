<template>
  <div class="pending-approval-container text-center">
    <div class="pending-approval-card">
      <NeoIcon name="clock" size="64" class="text-warning mb-4" />
      <h1>Pending Approval</h1>
      <p class="lead">Your account is currently under review by our administrators.</p>
      <p>We'll notify you once your account has been approved. This usually takes 1-2 business days.</p>

      <div class="action-buttons mt-4">
        <NeoButton variant="secondary" @click="logout">Logout</NeoButton>
      </div>
    </div>
  </div>
</template>

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

<style scoped>
.pending-approval-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
}

.pending-approval-card {
  width: 100%;
  max-width: 500px;
}

.message {
  font-size: 1.2rem;
  font-weight: 500;
  color: #343a40;
}

.sub-message {
  color: #6c757d;
  margin-bottom: 1rem;
}

.pending-icon {
  font-size: 3rem;
  color: #ffd700;
}
</style>
