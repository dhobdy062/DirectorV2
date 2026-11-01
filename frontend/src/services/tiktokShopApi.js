import axios from "axios";
import { SEED_TRENDING_VIDEOS } from "../lib/tiktokShop/seedTrendingVideos.js";
import { rankTrendingVideos } from "../lib/tiktokShop/trendingMetrics.js";

const http = axios.create({
  timeout: 15000,
});

export async function fetchTrendingVideos({ backendUrl, collectionId, useSeed = true }) {
  if (!backendUrl || !collectionId) {
    if (!useSeed) {
      return [];
    }
    return rankTrendingVideos(SEED_TRENDING_VIDEOS);
  }

  try {
    const { data } = await http.get(
      `${backendUrl}/videodb/collection/${collectionId}/video`,
    );
    const videos = (data?.videos ?? data ?? []).map(mapCollectionVideo);
    if (videos.length === 0 && useSeed) {
      return rankTrendingVideos(SEED_TRENDING_VIDEOS);
    }
    return rankTrendingVideos(videos);
  } catch {
    return rankTrendingVideos(SEED_TRENDING_VIDEOS);
  }
}

function mapCollectionVideo(video) {
  return {
    id: video.id ?? video.video_id,
    title: video.name ?? video.title ?? "Untitled reference",
    creator: video.metadata?.creator ?? "@reference",
    category: video.metadata?.category ?? "General",
    views: video.metadata?.views ?? 50000,
    engagementRate: video.metadata?.engagement_rate ?? 0.06,
    shopClickRate: video.metadata?.shop_click_rate ?? 0.04,
    gmvLift: video.metadata?.gmv_lift ?? 0.08,
    hookType: video.metadata?.hook_type ?? "curiosity_gap",
    hasProductDemo: video.metadata?.has_product_demo ?? true,
    ctaSecond: video.metadata?.cta_second ?? 10,
    durationSeconds: video.length ?? video.duration ?? 28,
    thumbnailHue: "indigo",
  };
}
