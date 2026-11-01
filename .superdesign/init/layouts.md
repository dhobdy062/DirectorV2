# Layouts

## frontend/src/App.vue
Root shell — full viewport `router-view` wrapper with popper theme CSS variables.

```vue
<script setup>
import "./style.css";
</script>

<template>
  <div class="w-full h-full template">
    <router-view />
  </div>
</template>
```

## frontend/src/views/TikTokShopStudioView.vue
Primary layout for TikTok Shop workflow: header, tabs, three step panels (discover → evaluate → template).

## frontend/src/views/DefaultView.vue
Full-height Perspxtv chat layout using `@videodb/chat-vue` ChatInterface.
