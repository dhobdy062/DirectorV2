/**
 * Tailwind CSS Animation Configuration
 * Extracted from main tailwind.config.js for better maintainability
 */

export const keyframes = {
  "accordion-down": {
    from: { height: "0" },
    to: { height: "var(--radix-accordion-content-height)" },
  },
  "accordion-up": {
    from: { height: "var(--radix-accordion-content-height)" },
    to: { height: "0" },
  },
  "caret-blink": {
    "0%,70%,100%": { opacity: "1" },
    "20%,50%": { opacity: "0" },
  },
};

export const animation = {
  "accordion-down": "accordion-down 0.2s ease-out",
  "accordion-up": "accordion-up 0.2s ease-out",
  "caret-blink": "caret-blink 1.25s ease-out infinite",
};
