<script setup>
import { ref } from 'vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoIcon from '@/components/ui/NeoIcon.vue'

const featuredServices = ref([
  {
    id: 1,
    name: 'Plumbing',
    description: 'Professional plumbing services for your home',
    icon: 'droplet',
    color: 'primary',
    rotation: '-3deg',
  },
  {
    id: 2,
    name: 'Electrical',
    description: 'Reliable electrical repair and installation services',
    icon: 'lightbulb',
    color: 'warning',
    rotation: '2deg',
  },
  {
    id: 3,
    name: 'Cleaning',
    description: 'Complete home cleaning and sanitization services',
    icon: 'brush',
    color: 'info',
    rotation: '-2deg',
  },
  {
    id: 4,
    name: 'Gardening',
    description: 'Professional garden maintenance and landscaping',
    icon: 'flower',
    color: 'success',
    rotation: '3deg',
  },
])

const testimonials = ref([
  {
    id: 1,
    name: 'John Smith',
    text: 'The service was excellent! The technician arrived on time and fixed my plumbing issue quickly.',
    rating: 5,
    color: 'primary',
    rotation: '2deg',
  },
  {
    id: 2,
    name: 'Emily Jones',
    text: "I'm very satisfied with the cleaning service. My house has never looked better!",
    rating: 5,
    color: 'warning',
    rotation: '-3deg',
  },
  {
    id: 3,
    name: 'Michael Brown',
    text: 'The gardening team did an amazing job with my backyard. Very professional service.',
    rating: 4,
    color: 'info',
    rotation: '1deg',
  },
])
</script>

<template>
  <div class="neo-brutalist-wrapper">
    <!-- Hero Section -->
    <div class="hero-section p-5 mb-5">
      <div class="container-fluid">
        <div class="row align-items-center">
          <div class="col-md-7">
            <div class="hero-text-container">
              <div class="title-block">
                <h1 class="display-1 fw-black mb-0">
                  <span class="duck-emoji">🦆</span> <span class="quack-title">QUACK!</span>
                </h1>
              </div>
              <p class="lead fw-bold mb-3 neo-subtitle">YOUR ONE-STOP SERVICE SOLUTION</p>
              <div class="hero-description p-3 mb-5">
                <p class="mb-0">
                  Find reliable professionals for plumbing, electrical work, cleaning, gardening,
                  and more!
                </p>
              </div>
              <div class="d-flex gap-4 flex-wrap">
                <router-link to="/register">
                  <NeoButton variant="warning" size="lg">GET STARTED</NeoButton>
                </router-link>
                <router-link to="/customer/services">
                  <NeoButton variant="success" size="lg">BROWSE SERVICES</NeoButton>
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-md-5 d-none d-md-block">
            <div class="hero-card-container">
              <NeoCard variant="primary" class="text-center hero-card">
                <NeoIcon name="wrench" size="160" />
              </NeoCard>
              <div class="hero-pattern-1"></div>
              <div class="hero-pattern-2"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Featured Services Section -->
    <section class="services-section mb-5 pb-5">
      <div class="container">
        <div class="section-heading-container">
          <h2 class="text-center mb-5 fw-black neo-section-title">OUR SERVICES</h2>
        </div>
        <div class="row g-4 justify-content-center">
          <div v-for="service in featuredServices" :key="service.id" class="col-md-6 col-lg-3">
            <NeoCard :variant="service.color" class="service-card h-100"
              :style="{ transform: `rotate(${service.rotation})` }">
              <template #title>
                <div class="text-center">
                  <div class="icon-wrapper mb-3">
                    <NeoIcon :name="service.icon" size="48" />
                  </div>
                  <h5 class="fw-bold text-uppercase service-name">{{ service.name }}</h5>
                </div>
              </template>
              <p class="text-center service-desc">{{ service.description }}</p>
              <template #footer>
                <div class="text-center">
                  <router-link to="/customer/services">
                    <NeoButton variant="dark" size="lg">BOOK NOW</NeoButton>
                  </router-link>
                </div>
              </template>
            </NeoCard>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="process-section py-5 mb-5">
      <div class="container">
        <div class="section-heading-container">
          <h2 class="text-center mb-5 fw-black neo-section-title">HOW IT WORKS</h2>
        </div>
        <div class="row text-center g-4 process-row">
          <div class="col-md-4">
            <div class="process-step" style="transform: rotate(-2deg)">
              <NeoCard variant="success" class="mb-3 process-card">
                <NeoIcon name="search" size="56" />
              </NeoCard>
              <div class="step-number">1</div>
              <h4 class="fw-bold text-uppercase mt-4 process-title">Search</h4>
              <p class="process-desc">
                Search for the service you need from our wide range of options
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="process-step" style="transform: rotate(2deg)">
              <NeoCard variant="info" class="mb-3 process-card">
                <NeoIcon name="calendar-check" size="56" />
              </NeoCard>
              <div class="step-number">2</div>
              <h4 class="fw-bold text-uppercase mt-4 process-title">Book</h4>
              <p class="process-desc">Book a service with your preferred time and date</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="process-step" style="transform: rotate(-1deg)">
              <NeoCard variant="warning" class="mb-3 process-card">
                <NeoIcon name="star" size="56" />
              </NeoCard>
              <div class="step-number">3</div>
              <h4 class="fw-bold text-uppercase mt-4 process-title">Enjoy</h4>
              <p class="process-desc">Enjoy quality service and share your experience</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section mb-5 pb-5">
      <div class="container">
        <div class="section-heading-container">
          <h2 class="text-center mb-5 fw-black neo-section-title">HAPPY CUSTOMERS</h2>
        </div>
        <div class="row g-4 justify-content-center">
          <div v-for="testimonial in testimonials" :key="testimonial.id" class="col-md-4">
            <NeoCard :variant="testimonial.color" class="testimonial-card h-100"
              :style="{ transform: `rotate(${testimonial.rotation})` }">
              <div class="rating mb-3">
                <NeoIcon v-for="i in testimonial.rating" :key="i" name="star" size="20" color="#000" />
              </div>
              <p class="fw-bold testimonial-text">"{{ testimonial.text }}"</p>
              <p class="text-end fw-black text-uppercase testimonial-name">
                - {{ testimonial.name }}
              </p>
            </NeoCard>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-5 mb-5">
      <div class="container text-center">
        <div class="cta-container p-5">
          <h2 class="mb-3 fw-black text-uppercase cta-title">Ready to get started?</h2>
          <p class="lead mb-4 fw-bold cta-subtitle">Join thousands of satisfied customers today!</p>
          <div class="d-flex justify-content-center gap-4 flex-wrap">
            <router-link to="/register">
              <NeoButton variant="danger" size="lg">SIGN UP NOW</NeoButton>
            </router-link>
            <router-link to="/login">
              <NeoButton variant="primary" size="lg">LOGIN</NeoButton>
            </router-link>
          </div>
        </div>
        <div class="cta-pattern-1"></div>
        <div class="cta-pattern-2"></div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.neo-brutalist-wrapper {
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
  overflow-y: auto;
  height: calc(100vh - 72px);
  position: relative;
}

/* General Styles */
.neo-section-title {
  font-size: 3.5rem;
  letter-spacing: 2px;
  position: relative;
  display: inline-block;
  padding: 0.5rem 2rem;
  background-color: #ffd700;
  border: 3px solid #000;
  box-shadow: 8px 8px 0 #000;
  transform: rotate(-1deg);
}

.section-heading-container {
  text-align: center;
  margin-bottom: 4rem;
}

/* Hero Section */
.hero-section {
  background-color: #ff7f50;
  position: relative;
  padding-top: 5rem !important;
  padding-bottom: 5rem !important;
  overflow: hidden;
  border-bottom: 5px solid #000;
}



.hero-text-container {
  position: relative;
  z-index: 10;
}

.title-block {
  margin-bottom: 2rem;
  display: inline-block;
}

.quack-title {
  font-size: 7rem;
  line-height: 1;
  letter-spacing: -2px;
  color: #000;
  text-shadow:
    5px 5px 0 #ffd700,
    8px 8px 0 #000;
  transform: rotate(-3deg);
  display: inline-block;
}

.duck-emoji {
  font-size: 7rem;
  display: inline-block;
  transform: rotate(10deg);
  position: relative;
  top: -10px;
  filter: drop-shadow(5px 5px 0 #000);
}

.neo-subtitle {
  font-size: 1.8rem;
  background-color: #000;
  color: #fff;
  padding: 0.75rem 1.5rem;
  display: inline-block;
  transform: rotate(1deg);
  box-shadow: 5px 5px 0 #ffd700;
}

.hero-description {
  background-color: white;
  border: 3px solid #000;
  box-shadow: 5px 5px 0 #000;
  max-width: 500px;
  transform: rotate(-1deg);
  font-size: 1.2rem;
  font-weight: bold;
}

.hero-card-container {
  position: relative;
  padding: 20px;
}

.hero-card {
  transform: rotate(5deg);
  z-index: 10;
  position: relative;
}

.hero-pattern-1,
.hero-pattern-2 {
  position: absolute;
  border: 3px solid #000;
  z-index: 1;
}

.hero-pattern-1 {
  width: 150px;
  height: 150px;
  background-color: #ffd700;
  top: 0;
  right: 50px;
  transform: rotate(25deg);
}

.hero-pattern-2 {
  width: 100px;
  height: 100px;
  background-color: #00ff7f;
  bottom: 30px;
  left: 20px;
  transform: rotate(-15deg);
}

/* Services Section */
.services-section {
  background-color: #fff;
  position: relative;
}

.service-card {
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-10px) rotate(0deg) !important;
}

.icon-wrapper {
  background-color: white;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 3px solid #000;
}

.service-name {
  font-size: 1.5rem;
  letter-spacing: 1px;
}

.service-desc {
  font-weight: 600;
  font-size: 1.1rem;
}

/* Process Section */
.process-section {
  background-color: #7fffd4;
  border-top: 5px solid #000;
  border-bottom: 5px solid #000;
  position: relative;
}

.process-row {
  position: relative;
  z-index: 10;
}

.process-step {
  transition: transform 0.3s ease;
}

.process-step:hover {
  transform: translateY(-10px) rotate(0deg) !important;
}

.process-card {
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-number {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 50px;
  height: 50px;
  background-color: #ff5555;
  border: 3px solid #000;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 900;
  z-index: 20;
}

.process-title {
  font-size: 1.8rem;
}

.process-desc {
  font-weight: 600;
  font-size: 1.1rem;
}

/* Testimonials Section */
.testimonials-section {
  background-color: #fff;
}

.testimonial-card {
  transition: transform 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-10px) rotate(0deg) !important;
}

.rating {
  font-size: 1.5rem;
}

.testimonial-text {
  font-size: 1.1rem;
  line-height: 1.6;
}

.testimonial-name {
  font-size: 1.2rem;
}

/* CTA Section */
.cta-section {
  background-color: #ff5555;
  position: relative;
  overflow: hidden;
  border-top: 5px solid #000;
  border-bottom: 5px solid #000;
}

.cta-container {
  background-color: white;
  border: 5px solid #000;
  box-shadow: 15px 15px 0 #000;
  position: relative;
  z-index: 10;
  max-width: 800px;
  margin: 0 auto;
  transform: rotate(-1deg);
}

.cta-title {
  font-size: 3rem;
  color: #000;
}

.cta-subtitle {
  font-size: 1.5rem;
}

.cta-pattern-1,
.cta-pattern-2 {
  position: absolute;
  border: 3px solid #000;
  z-index: 1;
}

.cta-pattern-1 {
  width: 120px;
  height: 120px;
  background-color: #ffd700;
  top: 50px;
  left: 10%;
  transform: rotate(25deg);
}

.cta-pattern-2 {
  width: 80px;
  height: 80px;
  background-color: #00ff7f;
  bottom: 30px;
  right: 10%;
  transform: rotate(-15deg);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .quack-title {
    font-size: 5rem;
  }

  .duck-emoji {
    font-size: 5rem;
  }

  .neo-section-title {
    font-size: 2.5rem;
  }

  .cta-title {
    font-size: 2.5rem;
  }

  .service-card,
  .testimonial-card,
  .process-step {
    transform: rotate(0deg) !important;
  }

  .neo-subtitle {
    font-size: 1.4rem;
  }
}
</style>
