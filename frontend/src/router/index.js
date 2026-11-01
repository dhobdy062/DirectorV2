import { createRouter, createWebHistory } from "vue-router";
import DefaultView from "../views/DefaultView.vue";
import TikTokShopStudioView from "../views/TikTokShopStudioView.vue";

const routes = [
  {
    path: "/",
    name: "TikTokShopStudio",
    component: TikTokShopStudioView,
  },
  {
    path: "/director",
    name: "DirectorChat",
    component: DefaultView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
