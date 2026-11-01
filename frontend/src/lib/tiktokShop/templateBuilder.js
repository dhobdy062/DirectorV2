function uniquePatterns(evaluations, dimensionKey) {
  const patterns = evaluations
    .map((entry) => entry.evaluation.dimensions[dimensionKey]?.pattern)
    .filter(Boolean);
  return [...new Set(patterns)];
}

function dominantStrength(evaluations, dimensionKey) {
  const strengths = evaluations.map(
    (entry) => entry.evaluation.dimensions[dimensionKey]?.strength,
  );
  if (strengths.includes("strong")) return "strong";
  if (strengths.includes("medium")) return "medium";
  return "weak";
}

export function buildShopVideoTemplate(evaluatedVideos) {
  const sorted = [...evaluatedVideos].sort(
    (a, b) => b.evaluation.overallScore - a.evaluation.overallScore,
  );
  const top = sorted.slice(0, 3);

  const hookPatterns = uniquePatterns(top, "hook");
  const productPatterns = uniquePatterns(top, "product");
  const ctaPatterns = uniquePatterns(top, "cta");

  const structure = {
    hook: {
      durationSeconds: 3,
      patterns: hookPatterns,
      strength: dominantStrength(top, "hook"),
      guidance: "Lead with the highest-performing hook pattern from trending references.",
    },
    product: {
      durationSeconds: 12,
      patterns: productPatterns,
      strength: dominantStrength(top, "product"),
      guidance: "Demonstrate the product early with shop-visible pricing or offer.",
    },
    cta: {
      durationSeconds: 5,
      patterns: ctaPatterns,
      strength: dominantStrength(top, "cta"),
      guidance: "Pin TikTok Shop link and repeat the offer before the final second.",
    },
    scenes: [
      { beat: "Hook", seconds: "0-3", action: hookPatterns[0] ?? "curiosity_gap" },
      { beat: "Proof", seconds: "3-15", action: productPatterns[0] ?? "demo_first" },
      { beat: "Offer", seconds: "15-22", action: "social_proof_or_results" },
      { beat: "CTA", seconds: "22-28", action: ctaPatterns[0] ?? "shop_link_early" },
    ],
  };

  const referenceIds = top.map((v) => v.id);

  return {
    name: "TikTok Shop Viral Template",
    referenceVideoIds: referenceIds,
    structure,
    checklist: [
      "Vertical 9:16, under 30 seconds",
      "Product visible before second 5",
      "On-screen price or bundle callout",
      "TikTok Shop link in caption and pinned comment",
    ],
    agentPrompt: [
      "Run viral_pattern_analysis on referenceVideoIds, then tiktok_script_generator",
      `Reference videos: ${referenceIds.join(", ")}`,
      `Hook patterns: ${hookPatterns.join(", ")}`,
      `Product patterns: ${productPatterns.join(", ")}`,
      `CTA patterns: ${ctaPatterns.join(", ")}`,
    ].join("\n"),
  };
}
