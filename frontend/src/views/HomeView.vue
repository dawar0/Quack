<script setup>
import { ref } from 'vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
// Sample featured services
const featuredServices = ref([
  {
    id: 1,
    name: 'Plumbing',
    description: 'Professional plumbing services for your home',
    icon: 'bi-droplet',
  },
  {
    id: 2,
    name: 'Electrical',
    description: 'Reliable electrical repair and installation services',
    icon: 'bi-lightning',
  },
  {
    id: 3,
    name: 'Cleaning',
    description: 'Complete home cleaning and sanitization services',
    icon: 'bi-brush',
  },
  {
    id: 4,
    name: 'Gardening',
    description: 'Professional garden maintenance and landscaping',
    icon: 'bi-flower1',
  },
])

// Sample testimonials
const testimonials = ref([
  {
    id: 1,
    name: 'John Smith',
    text: 'The service was excellent! The technician arrived on time and fixed my plumbing issue quickly.',
    rating: 5,
  },
  {
    id: 2,
    name: 'Emily Jones',
    text: "I'm very satisfied with the cleaning service. My house has never looked better!",
    rating: 5,
  },
  {
    id: 3,
    name: 'Michael Brown',
    text: 'The gardening team did an amazing job with my backyard. Very professional service.',
    rating: 4,
  },
])
</script>

<template>
  <div class="neo-brutalist container">
    <!-- Hero Section -->
    <div class="hero-section bg-black text-white p-5 mb-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="display-1 fw-black mb-4">🦆 Quack</h1>
            <p class="lead fw-bold mb-4">Your one-stop solution for all household services</p>
            <p class="mb-4">
              Find reliable professionals for plumbing, electrical work, cleaning, gardening, and
              more!
            </p>
            <div class="d-flex gap-3">
              <router-link to="/register">
                <NeoButton variant="primary" size="lg">Get Started</NeoButton>
              </router-link>
              <router-link to="/customer/services">
                <NeoButton variant="primary" size="lg" outline>Browse Services</NeoButton>
              </router-link>
            </div>
          </div>
          <div class="col-md-6 d-none d-md-block">
            <NeoCard variant="primary" class="text-center">
              <i class="bi bi-tools text-black" style="font-size: 8rem"></i>
            </NeoCard>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Services Section -->
    <section class="mb-5">
      <div class="container">
        <h2 class="text-center mb-5 fw-black text-uppercase">Our Services</h2>
        <div class="row g-4">
          <div v-for="service in featuredServices" :key="service.id" class="col-md-3">
            <NeoCard>
              <template #title>
                <div class="text-center">
                  <i :class="service.icon" class="bi text-black mb-3" style="font-size: 2.5rem"></i>
                  <h5 class="fw-bold text-uppercase">{{ service.name }}</h5>
                </div>
              </template>
              <p class="text-center">{{ service.description }}</p>
              <template #footer>
                <div class="text-center">
                  <router-link to="/customer/services">
                    <NeoButton variant="dark" size="lg">Book Now</NeoButton>
                  </router-link>
                </div>
              </template>
            </NeoCard>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="bg-black text-white py-5 mb-5">
      <div class="container">
        <h2 class="text-center mb-5 fw-black text-uppercase">How It Works</h2>
        <div class="row text-center g-4">
          <div class="col-md-4">
            <NeoCard variant="success" class="mb-3">
              <i class="bi bi-search" style="font-size: 2.5rem"></i>
            </NeoCard>
            <h4 class="fw-bold text-uppercase">Search</h4>
            <p>Search for the service you need from our wide range of options</p>
          </div>
          <div class="col-md-4">
            <NeoCard variant="info" class="mb-3">
              <i class="bi bi-calendar-check" style="font-size: 2.5rem"></i>
            </NeoCard>
            <h4 class="fw-bold text-uppercase">Book</h4>
            <p>Book a service with your preferred time and date</p>
          </div>
          <div class="col-md-4">
            <NeoCard variant="warning" class="mb-3">
              <i class="bi bi-star" style="font-size: 2.5rem"></i>
            </NeoCard>
            <h4 class="fw-bold text-uppercase">Enjoy & Review</h4>
            <p>Enjoy quality service and share your experience</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="mb-5">
      <div class="container">
        <h2 class="text-center mb-5 fw-black text-uppercase">What Our Customers Say</h2>
        <div class="row g-4">
          <div v-for="testimonial in testimonials" :key="testimonial.id" class="col-md-4">
            <NeoCard>
              <div class="mb-3">
                <i v-for="i in testimonial.rating" :key="i" class="bi bi-star-fill text-black"></i>
              </div>
              <p class="fw-bold">"{{ testimonial.text }}"</p>
              <p class="text-end fw-black text-uppercase">- {{ testimonial.name }}</p>
            </NeoCard>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-black text-white py-5 mb-5">
      <div class="container text-center">
        <h2 class="mb-3 fw-black text-uppercase">Ready to get started?</h2>
        <p class="lead mb-4 fw-bold">Join thousands of satisfied customers today!</p>
        <div class="d-flex justify-content-center gap-3">
          <router-link to="/register">
            <NeoButton variant="primary" size="lg">Sign Up Now</NeoButton>
          </router-link>
          <router-link to="/login">
            <NeoButton variant="primary" size="lg" outline>Login</NeoButton>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.neo-brutalist {
  font-family: 'Inter', sans-serif;
}

.neo-brutalist .display-1 {
  font-size: 4rem;
  line-height: 1.1;
}

.neo-brutalist .lead {
  font-size: 1.5rem;
}

.neo-brutalist section {
  padding: 5rem 0;
}

.neo-brutalist a {
  text-decoration: none;
}
</style>
