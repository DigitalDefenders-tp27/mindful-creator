<template>
  <component
    :is="is"
    :class="
      cn(
        'rainbow-button',
        'group relative inline-flex cursor-pointer items-center justify-center rounded-xl border-2 bg-[length:200%] px-4 py-2 font-medium transition-colors [background-clip:padding-box,border-box,border-box] [background-origin:border-box] [border:calc(0.12*1rem)_solid_transparent] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
        'before:absolute before:bottom-[-20%] before:left-1/2 before:z-0 before:h-1/5 before:w-3/5 before:-translate-x-1/2 before:bg-[linear-gradient(90deg,var(--color-1),var(--color-5),var(--color-3),var(--color-4),var(--color-2))] before:bg-[length:200%] before:[filter:blur(calc(0.8*1rem))]',
        'bg-[linear-gradient(white,white),linear-gradient(white_50%,rgba(255,255,255,0.6)_80%,rgba(255,255,255,0)),linear-gradient(90deg,var(--color-1),var(--color-5),var(--color-3),var(--color-4),var(--color-2))]',
        'dark:bg-[linear-gradient(white,white),linear-gradient(white_50%,rgba(255,255,255,0.6)_80%,rgba(255,255,255,0)),linear-gradient(90deg,var(--color-1),var(--color-5),var(--color-3),var(--color-4),var(--color-2))]',
        props.class,
      )
    "
  >
    <slot />
  </component>
</template>

<script setup lang="ts">
import { cn } from "@/lib/utils";
import { computed } from "vue";

interface RainbowButtonProps {
  class?: string;
  is?: string;
  speed?: number;
}

const props = withDefaults(defineProps<RainbowButtonProps>(), {
  speed: 2,
  is: "button",
});

const speedInSeconds = computed(() => `${props.speed}s`);
</script>

<style scoped>
.rainbow-button {
  --color-1: hsl(142, 76%, 36%); /* Main green color - match with the site's theme */
  --color-2: hsl(210, 100%, 63%);
  --color-3: hsl(270, 100%, 63%);
  --color-4: hsl(20, 100%, 63%);
  --color-5: hsl(90, 100%, 63%);
  --speed: v-bind(speedInSeconds);
  animation: rainbow var(--speed) infinite linear;
  letter-spacing: 0.5px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

.rainbow-button:before {
  animation: rainbow var(--speed) infinite linear;
  filter: blur(12px);
  opacity: 0.4;
}

.rainbow-button {
  background-color: white !important;
  border: 3px solid transparent;
  background-clip: padding-box, border-box, border-box;
  background-origin: border-box;
  color: #111 !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.07);
}

@keyframes rainbow {
  0% {
    background-position: 0;
  }
  100% {
    background-position: 200%;
  }
}
</style> 