const HOOK_WEIGHTS = {
  curiosity_gap: 18,
  visual_reveal: 16,
  transformation: 15,
  price_shock: 14,
  testimonial: 12,
  slow_intro: 4,
};

function scoreDimension(value, max) {
  return Math.round(clamp(value, 0, max));
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function strengthFromScore(score) {
  if (score >= 75) return "strong";
  if (score >= 50) return "medium";
  return "weak";
}

export function evaluateTrendingVideo(video) {
  const hookBase = HOOK_WEIGHTS[video.hookType] ?? 8;
  const hookScore = scoreDimension(hookBase + (video.shopClickRate ?? 0) * 120, 25);

  const productScore = scoreDimension(
    (video.hasProductDemo ? 18 : 4) + (video.shopClickRate ?? 0) * 80,
    25,
  );

  const idealCta = 10;
  const ctaDelta = Math.abs((video.ctaSecond ?? idealCta) - idealCta);
  const ctaScore = scoreDimension(22 - ctaDelta * 1.4, 25);

  const pacingScore = scoreDimension(
    20 - Math.abs((video.durationSeconds ?? 30) - 28) * 0.6,
    25,
  );

  const overallScore = hookScore + productScore + ctaScore + pacingScore;

  const dimensions = {
    hook: {
      pattern: video.hookType,
      strength: strengthFromScore(hookScore * 4),
      score: hookScore,
    },
    product: {
      pattern: video.hasProductDemo ? "demo_first" : "mention_only",
      strength: strengthFromScore(productScore * 4),
      score: productScore,
    },
    cta: {
      pattern: (video.ctaSecond ?? 0) <= 12 ? "shop_link_early" : "shop_link_late",
      strength: strengthFromScore(ctaScore * 4),
      score: ctaScore,
    },
    pacing: {
      pattern: "short_form",
      strength: strengthFromScore(pacingScore * 4),
      score: pacingScore,
    },
  };

  const recommendations = [];
  if (dimensions.hook.strength !== "strong") {
    recommendations.push("Open with a curiosity gap or visual reveal in the first second.");
  }
  if (dimensions.product.strength !== "strong") {
    recommendations.push("Show the product in the first 5 seconds for TikTok Shop conversion.");
  }
  if (dimensions.cta.strength === "weak") {
    recommendations.push("Move the shop CTA before second 12.");
  }
  if (overallScore >= 70) {
    recommendations.push("Save as a template anchor — patterns are shop-ready.");
  }

  return {
    videoId: video.id,
    title: video.title,
    overallScore,
    dimensions,
    recommendations,
  };
}
