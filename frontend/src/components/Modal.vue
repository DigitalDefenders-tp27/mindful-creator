<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-window">
      <header v-if="$slots.header" class="modal-header">
        <slot name="header"></slot>
      </header>
      <section class="modal-body">
        <slot name="body"></slot>
      </section>
      <footer v-if="$slots.footer" class="modal-footer">
        <slot name="footer"></slot>
      </footer>
    </div>
  </div>
</template>

<script setup>
// No script needed for basic modal
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  z-index: 2000;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.2s;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
.modal-window {
  background: #fff;
  border-radius: 1.5rem;
  min-width: 320px;
  max-width: 95vw;
  min-height: 120px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 2rem 2rem 1.5rem 2rem;
  position: relative;
  animation: popIn 0.25s;
}
@keyframes popIn {
  from { transform: scale(0.95); opacity: 0.7; }
  to { transform: scale(1); opacity: 1; }
}
.modal-header {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  color: #e75a97;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.modal-body {
  font-size: 1.08rem;
  color: #444;
}
.modal-footer {
  margin-top: 1.5rem;
  text-align: right;
}
</style>
