<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
});
</script>

<template>
  <header class="bg-primary-900 text-white px-24 py-20 shadow-3">
    <p class="text-overline text-secondary-200">Perspxtv · TikTok Shop</p>
    <h1 class="text-heading1 font-semibold mt-4">{{ title }}</h1>
    <p v-if="subtitle" class="text-body text-white/80 mt-8 max-w-640">{{ subtitle }}</p>
  </header>
</template>
