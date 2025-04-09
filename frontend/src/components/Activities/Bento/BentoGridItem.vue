<template>
  <div
    :class="
      cn(
        'row-span-1 rounded-xl group/bento hover:shadow-xl transition duration-200 shadow-input dark:shadow-none dark:bg-black dark:border-white/[0.2] bg-white border border-transparent overflow-hidden flex flex-col',
        props.class,
      )
    "
    @click="$emit('click')"
    role="button"
    tabindex="0"
    :aria-label="ariaLabel"
  >
    <!-- 图片部分 - 占据卡片上部大部分空间 -->
    <div class="w-full h-48 overflow-hidden">
      <slot name="icon" />
    </div>
    
    <!-- 内容部分 - 只占据卡片底部 -->
    <div class="p-4 flex flex-col">
      <div class="font-sans font-bold text-neutral-600 dark:text-neutral-200 text-lg">
        <slot name="title" />
      </div>
      <div class="font-sans text-xs font-normal text-neutral-600 dark:text-neutral-300 mt-1">
        <slot name="description" />
      </div>
    </div>
    
    <slot name="header" />
  </div>
</template>

<script lang="ts" setup>
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

interface Props {
  class?: HTMLAttributes["class"];
  ariaLabel?: string;
  href?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['click']);

function handleClick(event: MouseEvent) {
  if (props.href) {
    window.open(props.href, '_blank');
  } else {
    emit('click', event);
  }
}
</script>

<style scoped>
div[role="button"] {
  cursor: pointer;
}

div[role="button"]:hover {
  transform: translateY(-3px);
}

div[role="button"]:active {
  transform: translateY(0);
}
</style>