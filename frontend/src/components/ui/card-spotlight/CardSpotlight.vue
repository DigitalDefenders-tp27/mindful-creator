<template>
  <div
    :class="[
      'group relative flex size-full overflow-hidden rounded-xl border bg-neutral-100 text-black dark:bg-neutral-900 dark:text-white transform-gpu transition-all duration-300 hover:scale-105 hover:shadow-lg',
      $props.class,
    ]"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    style="transform-style: preserve-3d; perspective: 1000px;"
  >
    <div :class="cn('relative z-10', props.slotClass)">
      <slot></slot>
    </div>
    <div
      class="pointer-events-none absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
      :style="{
        background: backgroundStyle,
        opacity: props.gradientOpacity,
      }"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { cn } from '@/lib/utils';

const props = defineProps({
  class: { type: String, default: '' },
  slotClass: { type: String, default: '' },
  gradientSize: { type: Number, default: 200 },
  gradientColor: { type: String, default: '#262626' },
  gradientOpacity: { type: Number, default: 0.8 },
});

const mouseX = ref(-props.gradientSize * 10);
const mouseY = ref(-props.gradientSize * 10);

function handleMouseMove(e) {
  const target = e.currentTarget;
  const rect = target.getBoundingClientRect();
  mouseX.value = e.clientX - rect.left;
  mouseY.value = e.clientY - rect.top;
}

function handleMouseLeave() {
  mouseX.value = -props.gradientSize * 10;
  mouseY.value = -props.gradientSize * 10;
}

onMounted(() => {
  mouseX.value = -props.gradientSize * 10;
  mouseY.value = -props.gradientSize * 10;
});

const backgroundStyle = computed(() => {
  return `radial-gradient(
    ${props.gradientSize}px circle at ${mouseX.value}px ${mouseY.value}px,
    ${props.gradientColor} 0%,
    rgba(0, 0, 0, 0) 70%
  )`;
});
</script>

<style scoped>
.group:hover {
  transform: translateY(-5px) rotateX(5deg);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

:deep(h3) {
  @apply text-xl font-semibold mb-4 text-neutral-900 dark:text-white;
}

:deep(p) {
  @apply text-neutral-600 dark:text-neutral-400;
}
</style>
