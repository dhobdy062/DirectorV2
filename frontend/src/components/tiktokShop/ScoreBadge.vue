<script setup>
defineProps({
  score: {
    type: Number,
    required: true,
  },
});
</script>

<template>
  <span
    class="inline-flex items-center rounded-8 px-8 py-4 text-caption1 font-semibold"
    :class="score >= 75 ? 'bg-green-100 text-green-800' : score >= 50 ? 'bg-amber-100 text-amber-900' : 'bg-red-100 text-red-800'"
  >
    {{ score }}
  </span>
</template>
