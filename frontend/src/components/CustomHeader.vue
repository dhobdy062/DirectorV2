<template>
  <header class="custom-header">
    <span class="logo-mark" aria-hidden="true">P</span>
    <h1 class="title">Perspxtv</h1>
  </header>
</template>

<script setup>
</script>

<style scoped>
.custom-header {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1e1b4b;
  color: #c4b5fd;
  box-shadow: 0 2px 4px rgba(30, 27, 75, 0.4);
}

.logo-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin-right: 1rem;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #c4b5fd);
  color: #fff;
  font-weight: 800;
  font-size: 1.25rem;
}

.title {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}
</style>
