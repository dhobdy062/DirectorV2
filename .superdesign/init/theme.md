# Theme tokens (summary)

- **Primary brand:** `#1E3A8A` (primary-800), light surfaces `#F0F4FF` (primary-100)
- **Secondary accent:** `#C4B5FD` (secondary DEFAULT)
- **Text:** textdark `#0F1D40`, textmedium `#525C76`, textlight `#8C93A3`
- **Font:** Inter (primary), Gilroy secondary
- **Radius:** 8px / 12px / 16px common (`rounded-8`, `rounded-12`)
- **Shadows:** subtle `shadow-1`, cards `shadow-2`

## Tailwind entry
`frontend/tailwind.config.js` extends modular `colors.js`, `theme.js`, `spacing.js`.

## Global CSS
`frontend/src/style.css` — Tailwind layers + body background `#f0f4ff`.
