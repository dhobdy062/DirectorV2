<script setup>
defineProps({
  evaluation: {
    type: Object,
    required: true,
  },
});
</script>

<template>
  <article class="rounded-12 border border-outline-xlight bg-white p-16 shadow-1">
    <header class="flex items-center justify-between gap-12 mb-12">
      <h3 class="text-subheader text-textdark">{{ evaluation.title }}</h3>
      <span class="text-heading2 text-primary-800 font-semibold">{{ evaluation.overallScore }}</span>
    </header>
    <dl class="grid grid-cols-2 gap-8 mb-12">
      <div v-for="(dim, key) in evaluation.dimensions" :key="key">
        <dt class="text-overline text-textlight">{{ key }}</dt>
        <dd class="text-body text-textdark capitalize">{{ dim.strength }} · {{ dim.pattern }}</dd>
      </div>
    </dl>
    <ul class="list-disc pl-16 text-caption1 text-textmedium space-y-4">
      <li v-for="tip in evaluation.recommendations" :key="tip">{{ tip }}</li>
    </ul>
  </article>
</template>
