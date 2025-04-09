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
    <!-- 图片部分 - 占据卡片上部大部分空间 / Image section - occupies most of the upper part of the card -->
    <div class="w-full h-48 overflow-hidden">
      <slot name="icon" />
    </div>
    
    <!-- 内容部分 - 只占据卡片底部 / Content section - only occupies the bottom of the card -->
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
// 导入工具函数和类型 / Import utility functions and types
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

// 组件属性接口定义 / Component props interface definition
interface Props {
  class?: HTMLAttributes["class"]; // 可选CSS类 / Optional CSS class
  ariaLabel?: string; // 可选的可访问性标签 / Optional accessibility label
  href?: string; // 可选链接地址 / Optional link URL
}

// 定义组件属性和事件 / Define component props and events
const props = defineProps<Props>();
const emit = defineEmits(['click']);

// 处理点击事件 / Handle click event
function handleClick(event: MouseEvent) {
  if (props.href) {
    window.open(props.href, '_blank');
  } else {
    emit('click', event);
  }
}
</script>

<style scoped>
/* 按钮样式 / Button styles */
div[role="button"] {
  cursor: pointer;
}

/* 悬停效果 - 上移 / Hover effect - move up */
div[role="button"]:hover {
  transform: translateY(-3px);
}

/* 点击效果 - 恢复位置 / Click effect - return to position */
div[role="button"]:active {
  transform: translateY(0);
}
</style>