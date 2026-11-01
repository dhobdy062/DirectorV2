import { describe, expect, it } from "vitest";
import {
  computeTrendScore,
  rankTrendingVideos,
} from "./trendingMetrics.js";

describe("computeTrendScore", () => {
  it("weights shop conversion signals higher than raw views", () => {
    const highViews = computeTrendScore({
      views: 500000,
      engagementRate: 0.04,
      shopClickRate: 0.01,
      gmvLift: 0.05,
    });
    const highShop = computeTrendScore({
      views: 120000,
      engagementRate: 0.11,
      shopClickRate: 0.09,
      gmvLift: 0.22,
    });

    expect(highShop).toBeGreaterThan(highViews);
  });
});

describe("rankTrendingVideos", () => {
  it("returns videos sorted by trend score descending", () => {
    const ranked = rankTrendingVideos([
      { id: "a", views: 1000, engagementRate: 0.02, shopClickRate: 0.01, gmvLift: 0.01 },
      { id: "b", views: 80000, engagementRate: 0.12, shopClickRate: 0.08, gmvLift: 0.18 },
      { id: "c", views: 40000, engagementRate: 0.07, shopClickRate: 0.04, gmvLift: 0.09 },
    ]);

    expect(ranked.map((v) => v.id)).toEqual(["b", "c", "a"]);
    expect(ranked[0].trendScore).toBeGreaterThan(ranked[1].trendScore);
  });
});
