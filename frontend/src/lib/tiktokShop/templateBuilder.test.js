import { describe, expect, it } from "vitest";
import { buildShopVideoTemplate } from "./templateBuilder.js";

describe("buildShopVideoTemplate", () => {
  it("merges top evaluations into a reusable TikTok Shop brief", () => {
    const template = buildShopVideoTemplate([
      {
        id: "1",
        title: "POV unboxing",
        evaluation: {
          overallScore: 88,
          dimensions: {
            hook: { pattern: "visual_reveal", strength: "strong" },
            product: { pattern: "demo_first", strength: "strong" },
            cta: { pattern: "shop_link_early", strength: "strong" },
          },
        },
      },
      {
        id: "2",
        title: "Before after",
        evaluation: {
          overallScore: 82,
          dimensions: {
            hook: { pattern: "transformation", strength: "strong" },
            product: { pattern: "benefit_stack", strength: "medium" },
            cta: { pattern: "urgency_offer", strength: "medium" },
          },
        },
      },
    ]);

    expect(template.name).toMatch(/TikTok Shop/i);
    expect(template.structure.hook.patterns.length).toBeGreaterThan(0);
    expect(template.structure.scenes.length).toBeGreaterThanOrEqual(3);
    expect(template.agentPrompt).toContain("viral_pattern_analysis");
  });
});
