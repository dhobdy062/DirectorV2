<script setup>
defineProps({
  template: {
    type: Object,
    required: true,
  },
});

defineEmits(["copy"]);
</script>

<template>
  <section class="rounded-16 border border-outline-xlight bg-white p-20 shadow-2 space-y-16">
    <header>
      <p class="text-overline text-textlight">Template blueprint</p>
      <h2 class="text-heading2 text-textdark">{{ template.name }}</h2>
    </header>
    <ol class="space-y-8">
      <li
        v-for="scene in template.structure.scenes"
        :key="scene.beat"
        class="flex gap-12 items-baseline border-l-4 border-primary-400 pl-12"
      >
        <span class="text-caption1 text-textlight w-48 shrink-0">{{ scene.seconds }}</span>
        <div>
          <p class="text-subheader text-textdark">{{ scene.beat }}</p>
          <p class="text-body text-textmedium">{{ scene.action }}</p>
        </div>
      </li>
    </ol>
    <button
      type="button"
      class="rounded-8 bg-primary-800 text-white px-16 py-10 text-body hover:bg-primary-900"
      @click="$emit('copy')"
    >
      Copy Perspxtv prompt
    </button>
  </section>
</template>
