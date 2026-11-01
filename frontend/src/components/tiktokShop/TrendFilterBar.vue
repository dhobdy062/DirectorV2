<script setup>
defineProps({
  category: {
    type: String,
    default: "all",
  },
  query: {
    type: String,
    default: "",
  },
});

defineEmits(["update:category", "update:query", "refresh"]);
</script>

<template>
  <div class="flex flex-wrap gap-12 items-end">
    <label class="flex flex-col gap-4 text-caption1 text-textmedium">
      Search trending
      <input
        :value="query"
        type="search"
        placeholder="Product, hook, creator…"
        class="rounded-8 border border-outline-medium px-12 py-8 min-w-220 text-body text-textdark"
        @input="$emit('update:query', $event.target.value)"
      />
    </label>
    <label class="flex flex-col gap-4 text-caption1 text-textmedium">
      Category
      <select
        :value="category"
        class="rounded-8 border border-outline-medium px-12 py-8 text-body text-textdark"
        @change="$emit('update:category', $event.target.value)"
      >
        <option value="all">All</option>
        <option value="Gadgets">Gadgets</option>
        <option value="Beauty">Beauty</option>
        <option value="Home">Home</option>
        <option value="Lifestyle">Lifestyle</option>
      </select>
    </label>
    <button
      type="button"
      class="rounded-8 border border-primary-800 text-primary-800 px-16 py-8 text-body hover:bg-primary-100"
      @click="$emit('refresh')"
    >
      Refresh trends
    </button>
  </div>
</template>
