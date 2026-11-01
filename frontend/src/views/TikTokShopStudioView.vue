<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import EvaluationDetailCard from "../components/tiktokShop/EvaluationDetailCard.vue";
import StudioNavTabs from "../components/tiktokShop/StudioNavTabs.vue";
import TemplateBlueprintPanel from "../components/tiktokShop/TemplateBlueprintPanel.vue";
import TikTokShopStudioHeader from "../components/tiktokShop/TikTokShopStudioHeader.vue";
import TrendFilterBar from "../components/tiktokShop/TrendFilterBar.vue";
import TrendVideoCard from "../components/tiktokShop/TrendVideoCard.vue";
import { useTikTokShopStudio } from "../composables/useTikTokShopStudio.js";

const router = useRouter();

const {
  activeTab,
  tabs,
  query,
  category,
  loading,
  filteredVideos,
  selectedIds,
  evaluations,
  template,
  loadTrending,
  toggleVideo,
  setTab,
} = useTikTokShopStudio();

onMounted(() => {
  loadTrending();
});

function copyTemplatePrompt() {
  if (!template.value) return;
  navigator.clipboard?.writeText(template.value.agentPrompt);
}

function openDirectorChat() {
  router.push({ name: "DirectorChat" });
}
</script>

<template>
  <div class="min-h-screen bg-primary-100 text-textdark flex flex-col">
    <TikTokShopStudioHeader
      title="Trend Lab for TikTok Shop"
      subtitle="Find trending shop videos, score what makes them convert, and export a Director template to produce similar content."
    />

    <div class="container py-20 flex-1 space-y-20">
      <StudioNavTabs :tabs="tabs" :active="activeTab" @change="setTab" />

      <section v-if="activeTab === 'discover'" class="space-y-16">
        <TrendFilterBar
          v-model:query="query"
          v-model:category="category"
          @refresh="loadTrending"
        />
        <p v-if="loading" class="text-body text-textmedium">Loading trending references…</p>
        <div v-else class="grid gap-12 md:grid-cols-2">
          <TrendVideoCard
            v-for="video in filteredVideos"
            :key="video.id"
            :video="video"
            :selected="selectedIds.has(video.id)"
            :evaluation="evaluations.get(video.id)"
            @toggle="toggleVideo"
          />
        </div>
        <p class="text-caption1 text-textlight">
          Select videos to evaluate — aim for 2–3 high trend scores in your niche.
        </p>
      </section>

      <section v-else-if="activeTab === 'evaluate'" class="space-y-16">
        <p v-if="evaluations.size === 0" class="text-body text-textmedium">
          No videos selected yet. Go to Discover and pick trending references.
        </p>
        <div v-else class="grid gap-16 lg:grid-cols-2">
          <EvaluationDetailCard
            v-for="evaluation in evaluations.values()"
            :key="evaluation.videoId"
            :evaluation="evaluation"
          />
        </div>
      </section>

      <section v-else class="space-y-16">
        <p v-if="!template" class="text-body text-textmedium">
          Select at least one evaluated video to generate a TikTok Shop template.
        </p>
        <TemplateBlueprintPanel v-else :template="template" @copy="copyTemplatePrompt" />
        <div class="flex gap-12 flex-wrap">
          <button
            type="button"
            class="rounded-8 bg-primary-800 text-white px-16 py-10 text-body"
            :disabled="!template"
            @click="openDirectorChat"
          >
            Open Director chat
          </button>
        </div>
      </section>
    </div>
  </div>
</template>
