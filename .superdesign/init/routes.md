# Routes

| Path | Name | Component | Purpose |
|------|------|-----------|---------|
| `/` | TikTokShopStudio | `views/TikTokShopStudioView.vue` | Trend discovery, evaluation, template export |
| `/chat` | PerspxtvChat | `views/DefaultView.vue` | Perspxtv agent chat |

```js
// frontend/src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import DefaultView from "../views/DefaultView.vue";
import TikTokShopStudioView from "../views/TikTokShopStudioView.vue";

const routes = [
  { path: "/", name: "TikTokShopStudio", component: TikTokShopStudioView },
  { path: "/chat", name: "PerspxtvChat", component: DefaultView },
];
```
