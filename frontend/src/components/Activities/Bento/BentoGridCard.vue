<template>
  <div
    :class="
      cn(
        'group relative rounded-2xl overflow-hidden flex flex-col justify-end transition-all duration-300',
        'bg-white/5 border border-white/10 shadow-xl hover:shadow-2xl h-full',
        'hover:-translate-y-1 hover:border-white/20',
        props.class
      )
    "
    @click="handleClick"
    role="button"
    tabindex="0"
    :aria-label="name"
  >
    <!-- 背景图片 / Background image -->
    <slot name="background"></slot>
    
    <!-- 渐变遮罩层 - 从下到上渐变 / Gradient overlay - bottom to top gradient -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent opacity-90 group-hover:opacity-70 transition-opacity duration-300 pointer-events-none"></div>
    
    <!-- 内容部分 / Content section -->
    <div class="relative z-10 p-6 text-left transform transition-transform duration-300 group-hover:translate-y-[-4px]">
      <h3 class="text-2xl font-bold text-white mb-2 group-hover:text-white/90">
        {{ name }}
      </h3>
      <p class="text-sm text-white/80 mb-4 line-clamp-2 group-hover:text-white/90">
        {{ description }}
      </p>
      <span
        v-if="cta"
        class="text-sm font-medium text-white/90 hover:text-white hover:underline inline-flex items-center gap-1"
      >
        {{ cta }}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M5 12h14"></path>
          <path d="m12 5 7 7-7 7"></path>
        </svg>
      </span>
    </div>
  </div>
</template>

<script lang="ts" setup>
// 导入工具函数和类型 / Import utility functions and types
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

// 组件属性接口定义 / Component props interface definition
interface Props {
  name: string; // 卡片标题 / Card title
  description: string; // 卡片描述 / Card description
  href?: string; // 可选链接 / Optional link
  image?: string; // 可选背景图片 / Optional background image
  cta?: string; // 可选号召性用语 / Optional call-to-action text
  class?: HTMLAttributes["class"]; // 可选CSS类 / Optional CSS classes
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
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  height: 100%;
}

/* 按钮点击效果 / Button click effect */
div[role="button"]:active {
  transform: translateY(0);
}

/* 限制描述文本行数 / Limit description text lines */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>