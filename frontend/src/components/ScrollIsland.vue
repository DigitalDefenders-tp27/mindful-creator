<template>
  <div
    class="fixed left-1/2 top-24 z-[999] -translate-x-1/2 backdrop-blur-lg border-radius"
    ref="islandRef"
    :style="{
      backgroundColor: 'rgba(231, 90, 151, 0.95)',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
      border: '1px solid rgba(255, 255, 255, 0.15)'
    }"
  >
    <div
      id="motion-id"
      class="relative cursor-pointer overflow-hidden text-white"
      :style="{
        borderRadius: borderRadius,
        height: open && isSlotAvailable ? '180px' : `${props.height}px`,
        width: open && isSlotAvailable ? '320px' : '260px',
        transition: 'height 0.4s cubic-bezier(0.16, 1, 0.3, 1), width 0.4s cubic-bezier(0.16, 1, 0.3, 1)'
      }"
    >
      <header 
        class="flex h-11 cursor-pointer items-center gap-2 px-4"
        @click="toggleOpen"
      >
        <div class="circular-progress">
          <svg width="24" height="24" viewBox="0 0 24 24">
            <circle
              cx="12"
              cy="12"
              r="10"
              fill="none"
              stroke="rgba(255,255,255,0.3)"
              stroke-width="2"
            />
            <circle
              cx="12"
              cy="12"
              r="10"
              fill="none"
              stroke="white"
              stroke-width="2"
              stroke-dasharray="62.83"
              :stroke-dashoffset="62.83 - (scrollPercentage * 62.83)"
              transform="rotate(-90 12 12)"
            />
          </svg>
        </div>
        <h1 class="grow text-center font-bold">{{ title }}</h1>
        <div class="percentage">{{ Math.round(scrollPercentage * 100) }}%</div>
      </header>
      <div
        class="content-container overflow-hidden"
        :style="{
          opacity: open ? 1 : 0,
          maxHeight: open ? '140px' : '0',
          transition: 'opacity 0.4s ease, max-height 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
          padding: open ? '0 12px 4px' : '0 12px'
        }"
      >
        <slot v-if="isSlotAvailable" />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, onUnmounted, ref, useSlots } from "vue";

interface Props {
  class?: string;
  title?: string;
  height?: number;
}

const props = withDefaults(defineProps<Props>(), {
  class: "",
  title: "Progress",
  height: 44,
});

const open = ref(false);
const slots = useSlots();
const islandRef = ref(null);

const scrollPercentage = ref(0);

const isSlotAvailable = computed(() => !!slots.default);
const borderRadius = computed(() => `${props.height / 2}px`);

// Function to toggle the island open/closed
const toggleOpen = () => {
  open.value = !open.value;
};

// Function to close the island
const closeIsland = () => {
  open.value = false;
};

// Define and expose closeIsland for external use
defineExpose({ closeIsland });

// Handler for document click to close island when clicking outside
const handleDocumentClick = (event) => {
  if (open.value && islandRef.value && !islandRef.value.contains(event.target)) {
    closeIsland();
  }
};

onMounted(() => {
  if (typeof window === "undefined") return;

  // Add event listeners
  window.addEventListener("scroll", updatePageScroll);
  document.addEventListener("click", handleDocumentClick);
  
  updatePageScroll();
});

function updatePageScroll() {
  scrollPercentage.value = window.scrollY / (document.body.scrollHeight - window.innerHeight);
}

onUnmounted(() => {
  // Remove event listeners
  window.removeEventListener("scroll", updatePageScroll);
  document.removeEventListener("click", handleDocumentClick);
});
</script>

<style scoped>
.border-radius {
  border-radius: v-bind(borderRadius);
}
</style> 