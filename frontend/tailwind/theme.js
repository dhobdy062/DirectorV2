/**
 * Tailwind CSS Theme Extensions
 * Extracted from main tailwind.config.js for better maintainability
 */

export const fontFamily = {
  primary: "Inter",
  secondary: "Gilroy",
  curgloria: "Gloria Hallelujah",
};

export const fontSize = {
  small: ["8px", "12px"],
  overline: [
    "10px",
    {
      lineHeight: "16px",
      letterSpacing: "0.04em",
      textTransform: "uppercase",
    },
  ],
  captionsm: ["10px", "12px"],
  caption2: ["10px", "16px"],
  caption18: ["10px", "20px"],
  caption15: ["12px", "14px"],
  caption1: ["12px", "20px"],
  caption3: ["11px", "16px"],
  body: ["14px", "24px"],
  subheader: ["16px", "24px"],
  subheader2: ["18px", "20px"],
  title: ["20px", "28px"],
  heading2: ["24px", "36px"],
  heading1: ["28px", "40px"],
  display6: ["30px", "35px"],
  display5: ["36px", "48px"],
  display4: ["48px", "56px"],
  display3: ["56px", "64px"],
  display2: ["64px", "72px"],
  display1: ["80px", "88px"],
};

export const borderRadius = {
  2: "2px",
  4: "4px",
  6: "6px",
  8: "8px",
  12: "12px",
  16: "16px",
  20: "20px",
  24: "24px",
};

export const borderWidth = {
  DEFAULT: "1px",
  0: "0",
  2: "2px",
  3: "3px",
  4: "4px",
  6: "6px",
  7: "7px",
  8: "8px",
};

export const boxShadow = {
  none: "none",
  1: "0px 1px 1px rgba(0, 0, 0, 0.1)",
  2: "0px 3px 3px rgba(0, 0, 0, 0.1)",
  3: "0px 6px 6px rgba(0, 0, 0, 0.08)",
  4: "0px 16px 16px rgba(0, 0, 0, 0.1)",
  5: "0px 32px 40px rgba(0, 0, 0, 0.1)",
  spextlg: "0px 5px 20px 1px rgba(0, 2, 40, 0.1)",
  searchbox: "0px 4px 18x 0.5x rgba(0, 2, 40, 0.1)",
  up2: "0px -3px 3px rgba(0, 0, 0, 0.08)",
  key: "0px 4px 16px rgba(0, 2, 40, 0.35)",
  lg: "0px 5px 20px 1px #DBE0E9",
  blur: "0px 0px 6px rgba(0,0,0,0.1)",
  "minimal-up": "0px -1px 5px rgba(0, 0, 0, 0.1)",
  "minimal-down": "0px 1px 5px rgba(0, 0, 0, 0.1)",
};

export const variants = {
  extend: {
    cursor: ["disabled"],
    opacity: ["group-hover"],
    backgroundColor: ["group-hover"],
    background: ["group-hover", "active"],
    display: ["group-hover"],
    border: ["group-hover", "active"],
    margin: ["group-hover"],
    padding: ["group-hover"],
    height: ["group-hover"],
    width: ["group-hover"],
    transform: ["group-hover"],
    scale: ["group-hover"],
    rotate: ["group-hover"],
    translate: ["group-hover"],
    skew: ["group-hover"],
    transitionProperty: ["group-hover"],
    transitionDuration: ["group-hover"],
    transitionTimingFunction: ["group-hover"],
    transitionDelay: ["group-hover"],
  },
};
