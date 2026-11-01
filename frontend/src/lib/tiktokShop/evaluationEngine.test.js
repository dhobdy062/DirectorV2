import { describe, expect, it } from "vitest";
import { evaluateTrendingVideo } from "./evaluationEngine.js";

describe("evaluateTrendingVideo", () => {
  it("scores TikTok Shop fit from hook, product clarity, and CTA timing", () => {
    const result = evaluateTrendingVideo({
      id: "vid-1",
      title: "3 reasons this $12 gadget sold out",
      hookType: "curiosity_gap",
      hasProductDemo: true,
      ctaSecond: 8,
      durationSeconds: 28,
      shopClickRate: 0.07,
    });

    expect(result.overallScore).toBeGreaterThanOrEqual(70);
    expect(result.dimensions.hook.strength).toBe("strong");
    expect(result.recommendations.some((r) => r.includes("template"))).toBe(true);
  });

  it("flags weak hooks and late CTAs for shop videos", () => {
    const result = evaluateTrendingVideo({
      id: "vid-2",
      title: "Random day vlog",
      hookType: "slow_intro",
      hasProductDemo: false,
      ctaSecond: 24,
      durationSeconds: 30,
      shopClickRate: 0.008,
    });

    expect(result.overallScore).toBeLessThan(50);
    expect(result.dimensions.cta.strength).toBe("weak");
  });
});
