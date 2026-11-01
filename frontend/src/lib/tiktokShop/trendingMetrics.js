const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

export function computeTrendScore(metrics) {
  const views = metrics.views ?? 0;
  const engagementRate = metrics.engagementRate ?? 0;
  const shopClickRate = metrics.shopClickRate ?? 0;
  const gmvLift = metrics.gmvLift ?? 0;

  const viewScore = clamp(Math.log10(views + 1) * 12, 0, 40);
  const engagementScore = clamp(engagementRate * 220, 0, 25);
  const shopScore = clamp(shopClickRate * 420, 0, 20);
  const gmvScore = clamp(gmvLift * 180, 0, 15);

  return Math.round(viewScore + engagementScore + shopScore + gmvScore);
}

export function rankTrendingVideos(videos) {
  return [...videos]
    .map((video) => ({
      ...video,
      trendScore: computeTrendScore(video),
    }))
    .sort((a, b) => b.trendScore - a.trendScore);
}
