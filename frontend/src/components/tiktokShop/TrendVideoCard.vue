<script setup>
import ScoreBadge from "./ScoreBadge.vue";

defineProps({
  video: {
    type: Object,
    required: true,
  },
  selected: {
    type: Boolean,
    default: false,
  },
  evaluation: {
    type: Object,
    default: null,
  },
});

defineEmits(["toggle"]);
</script>

<template>
  <button
    type="button"
    class="w-full text-left rounded-12 border p-12 transition shadow-1 hover:shadow-2"
    :class="selected ? 'border-primary-600 bg-primary-100' : 'border-outline-xlight bg-white'"
    @click="$emit('toggle', video.id)"
  >
    <div class="flex gap-12 items-start">
      <div
        class="w-56 h-80 rounded-8 shrink-0 bg-gradient-to-br from-primary-500 to-secondary-500 opacity-90"
      />
      <div class="flex-1 min-w-0">
        <p class="text-caption1 text-textlight uppercase">{{ video.category }}</p>
        <h3 class="text-subheader text-textdark truncate">{{ video.title }}</h3>
        <p class="text-caption1 text-textmedium mt-4">{{ video.creator }} · {{ video.views.toLocaleString() }} views</p>
        <div class="flex gap-8 mt-8 items-center flex-wrap">
          <span class="text-caption1 px-8 py-4 rounded-8 bg-primary-100 text-primary-800">Trend {{ video.trendScore }}</span>
          <ScoreBadge v-if="evaluation" :score="evaluation.overallScore" />
        </div>
      </div>
    </div>
  </button>
</template>
