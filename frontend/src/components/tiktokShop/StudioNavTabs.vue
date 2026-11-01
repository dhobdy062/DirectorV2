<script setup>
defineProps({
  tabs: {
    type: Array,
    required: true,
  },
  active: {
    type: String,
    required: true,
  },
});

defineEmits(["change"]);
</script>

<template>
  <nav class="flex gap-8 border-b border-outline-xlight">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      type="button"
      class="px-12 py-10 text-body border-b-2 transition-colors"
      :class="active === tab.id ? 'border-primary-800 text-primary-800' : 'border-transparent text-textmedium hover:text-textdark'"
      @click="$emit('change', tab.id)"
    >
      {{ tab.label }}
    </button>
  </nav>
</template>
