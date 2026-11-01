<script setup>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { ChatInterface } from "@videodb/chat-vue";
import "@videodb/chat-vue/dist/style.css";
import { createPerspxtvChatConfig } from "../config/perspxtvChatConfig.js";

const BACKEND_URL = import.meta.env.VITE_APP_BACKEND_URL ?? "";
const chatInterfaceRef = ref(null);
const chatConfig = computed(() => createPerspxtvChatConfig(BACKEND_URL));

const handleKeyDown = (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "k") {
    event.preventDefault();
    chatInterfaceRef.value.createNewSession();
    chatInterfaceRef.value.chatInputRef.focus();
  }
};
onMounted(() => {
  window.addEventListener("keydown", handleKeyDown);
});
onUnmounted(() => {
  window.removeEventListener("keydown", handleKeyDown);
});
</script>

<template>
  <main>
    <chat-interface
      ref="chatInterfaceRef"
      :chat-hook-config="chatConfig.chatHookConfig"
      :chat-input-placeholder="chatConfig.chatInputPlaceholder"
      :header-config="chatConfig.headerConfig"
      :sidebar-config="chatConfig.sidebarConfig"
      :default-screen-config="chatConfig.defaultScreenConfig"
    />
  </main>
</template>

<style>
:root {
  --popper-theme-background-color: #333333;
  --popper-theme-background-color-hover: #333333;
  --popper-theme-text-color: #ffffff;
  --popper-theme-border-width: 0px;
  --popper-theme-border-style: solid;
  --popper-theme-border-radius: 8px;
  --popper-theme-padding: 4px 8px;
  --popper-theme-box-shadow: 0px 6px 6px rgba(0, 0, 0, 0.08);
}

.template {
  height: 100vh;
  width: 100vw;
}

main {
  overflow: scroll;
  height: 100%;
}
html {
  overflow: hidden;
}

::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 6px;
  border: 3px solid #f1f1f1;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

* {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}
</style>
