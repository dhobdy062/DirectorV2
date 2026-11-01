import PerspxtvIcon from "../components/PerspxtvIcon.vue";

export function createPerspxtvChatConfig(backendUrl) {
  return {
    chatHookConfig: {
      socketUrl: `${backendUrl}/chat`,
      httpUrl: `${backendUrl}`,
      debug: true,
    },
    chatInputPlaceholder: "Ask Perspxtv",
    headerConfig: {
      uploadButton: true,
      headerText: "Perspxtv",
    },
    sidebarConfig: {
      enabled: true,
      icon: PerspxtvIcon,
      links: [
        {
          href: "/",
          text: "TikTok Shop Trend Lab",
        },
      ],
    },
    defaultScreenConfig: {
      enableVideoView: true,
      actionCardQueries: [
        {
          title: "Analyze viral TikTok Shop videos",
          query: "Analyze my trending shop videos for viral hooks and conversion patterns",
        },
        {
          title: "Build a shop video script",
          query: "Generate a TikTok Shop script from my product and top reference videos",
        },
        {
          title: "Create a similar video",
          query: "Create a TikTok Shop video similar to my best-performing references",
        },
      ],
      demoVideos: [],
    },
  };
}
