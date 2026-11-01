# Page dependency trees

## / (TikTok Shop Studio)
Entry: `frontend/src/views/TikTokShopStudioView.vue`
Dependencies:
- `frontend/src/composables/useTikTokShopStudio.js`
  - `frontend/src/lib/tiktokShop/evaluationEngine.js`
  - `frontend/src/lib/tiktokShop/templateBuilder.js`
  - `frontend/src/services/tiktokShopApi.js`
    - `frontend/src/lib/tiktokShop/seedTrendingVideos.js`
    - `frontend/src/lib/tiktokShop/trendingMetrics.js`
- `frontend/src/components/tiktokShop/TikTokShopStudioHeader.vue`
- `frontend/src/components/tiktokShop/StudioNavTabs.vue`
- `frontend/src/components/tiktokShop/TrendFilterBar.vue`
- `frontend/src/components/tiktokShop/TrendVideoCard.vue`
  - `frontend/src/components/tiktokShop/ScoreBadge.vue`
- `frontend/src/components/tiktokShop/EvaluationDetailCard.vue`
- `frontend/src/components/tiktokShop/TemplateBlueprintPanel.vue`

## /chat (Agent chat)
Entry: `frontend/src/views/DefaultView.vue`
Dependencies:
- `@videodb/chat-vue` (external)
