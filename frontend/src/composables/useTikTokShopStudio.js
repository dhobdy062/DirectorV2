import { computed, ref } from "vue";
import { evaluateTrendingVideo } from "../lib/tiktokShop/evaluationEngine.js";
import { buildShopVideoTemplate } from "../lib/tiktokShop/templateBuilder.js";
import { fetchTrendingVideos } from "../services/tiktokShopApi.js";

export function useTikTokShopStudio() {
  const backendUrl = import.meta.env.VITE_APP_BACKEND_URL ?? "";
  const collectionId = import.meta.env.VITE_TIKTOK_SHOP_COLLECTION_ID ?? "";

  const activeTab = ref("discover");
  const query = ref("");
  const category = ref("all");
  const loading = ref(false);
  const videos = ref([]);
  const selectedIds = ref(new Set());

  const tabs = [
    { id: "discover", label: "Discover trends" },
    { id: "evaluate", label: "Evaluate" },
    { id: "template", label: "Template" },
  ];

  async function loadTrending() {
    loading.value = true;
    try {
      videos.value = await fetchTrendingVideos({ backendUrl, collectionId });
    } finally {
      loading.value = false;
    }
  }

  const filteredVideos = computed(() =>
    videos.value.filter((video) => {
      const matchesCategory =
        category.value === "all" || video.category === category.value;
      const q = query.value.trim().toLowerCase();
      const matchesQuery =
        !q ||
        video.title.toLowerCase().includes(q) ||
        video.creator.toLowerCase().includes(q);
      return matchesCategory && matchesQuery;
    }),
  );

  const evaluations = computed(() => {
    const map = new Map();
    for (const video of videos.value) {
      if (selectedIds.value.has(video.id)) {
        map.set(video.id, evaluateTrendingVideo(video));
      }
    }
    return map;
  });

  const selectedEvaluations = computed(() =>
    [...evaluations.value.values()].map((evaluation) => ({
      id: evaluation.videoId,
      title: evaluation.title,
      evaluation,
    })),
  );

  const template = computed(() => {
    if (selectedEvaluations.value.length === 0) {
      return null;
    }
    return buildShopVideoTemplate(selectedEvaluations.value);
  });

  function toggleVideo(id) {
    const next = new Set(selectedIds.value);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    selectedIds.value = next;
  }

  function setTab(tabId) {
    activeTab.value = tabId;
  }

  return {
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
  };
}
