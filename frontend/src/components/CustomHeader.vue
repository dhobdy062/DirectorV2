<template>
  <header class="custom-header">
    <img src="https://cdn.discordapp.com/attachments/1130919279279277632/1130919280110914098/tulbox-logo.png" alt="TULBOX Logo" class="logo" />
    <h1 class="title">TULBOX</h1>
  </header>
</template>

<script setup>
// No script needed for static header
</script>

<style scoped>
.custom-header {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #7aa1c8; /* Example: dark blue background */
  color: #020f7e; /* Example: orange text */
  box-shadow: 0 2px 4px rgba(177, 37, 37, 0.51);
}

.logo {
  height: 40px;
  margin-right: 1rem;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  font-family: 'Arial Black', Arial, sans-serif;
}
</style>
