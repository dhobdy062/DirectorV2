// Import modular configuration
const { colors } = require('./tailwind/colors.js');
const { spacing, minWidth, maxWidth } = require('./tailwind/spacing.js');
const { fontFamily, fontSize, borderRadius, borderWidth, boxShadow, variants } = require('./tailwind/theme.js');
const { safelist } = require('./tailwind/safelist.js');

module.exports = {
  content: ["./src/**/*.{html,js,vue, ts}"],
  options: {
    safelist,
  },
  enabled: true,
  theme: {
    fontFamily,
    minWidth,
    maxWidth,
    boxShadow,
    extend: {
      fontSize,
      spacing,
      borderRadius,
      borderWidth,
      colors,
    },
  },
  variants,
  corePlugins: {
    container: false,
  },
  plugins: [
    function ({ addComponents }) {
      addComponents({
        ".container": {
          maxWidth: "100%",
          paddingLeft: "20px",
          paddingRight: "20px",
          marginLeft: "auto",
          marginRight: "auto",

          "@screen sm": {
            maxWidth: "600px",
          },
          "@screen md": {
            maxWidth: "700px",
          },
          "@screen lg": {
            maxWidth: "1280px",
            paddingLeft: "56px",
            paddingRight: "56px",
          },
          "@screen xl": {
            maxWidth: "1344px",
          },
        },
      });
    },
  ],
};
