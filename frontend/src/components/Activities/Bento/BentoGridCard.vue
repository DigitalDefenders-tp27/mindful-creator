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
      <h3 class="text-2xl font-bold text-white mb-2 group-hover:text-white" style="color: white !important; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
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
  box-shadow: 0 4px 24px rgba(76, 201, 240, 0.08), 0 1.5px 8px rgba(0,0,0,0.06);
  background-color: #fff;
  position: relative;
  overflow: hidden;
  border-radius: 1.25rem;
  width: 100%;
  height: 100%;
}

div[role="button"]:hover {
  box-shadow: 0 8px 32px 0 rgba(76, 201, 240, 0.18), 0 4px 24px rgba(0,0,0,0.12);
  border: 2.5px solid #6CBDB5;
  transform: scale(1.035) translateY(-6px);
  z-index: 2;
}

/* 背景图片样式 / Background image styles */
.absolute.inset-0.bg-cover.bg-center {
  height: 100%;
  transition: transform 0.7s ease-out;
}

div[role="button"]:hover .absolute.inset-0.bg-cover.bg-center {
  transform: scale(1.1);
}

/* 内容区增强分割和阴影 */
.relative.z-10.p-6.text-left {
  background: rgba(255,255,255,0.12);
  border-radius: 1.25rem 1.25rem 0 0;
  box-shadow: 0 2px 16px 0 rgba(108,189,181,0.12);
  border-bottom: 2px solid rgba(108,189,181,0.20);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 110px;
  padding: 1.5rem;
  text-align: left;
  bottom: 0;
  width: 100%;
}

div[role="button"]:hover .relative.z-10.p-6.text-left {
  background: rgba(255,255,255,0.15);
  box-shadow: 0 4px 24px rgba(108,189,181,0.15);
}

/* 标题和描述文字样式 / Title and description text styles */
.relative.z-10.p-6.text-left h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.38);
  margin-bottom: 0.5rem;
  margin-top: 0;
  text-align: left;
  line-height: 1.3;
}

.relative.z-10.p-6.text-left p {
  font-size: 1.1rem;
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.28);
  margin: 0;
  line-height: 1.45;
  text-align: left;
  opacity: 0.95;
}

/* 渐变遮罩增强 / Enhanced gradient overlay */
.absolute.inset-0.bg-gradient-to-t {
  background: linear-gradient(
    to top,
    rgba(0,0,0,0.85) 0%,
    rgba(0,0,0,0.5) 35%,
    rgba(0,0,0,0.1) 100%
  );
  transition: opacity 0.3s ease;
}

div[role="button"]:hover .absolute.inset-0.bg-gradient-to-t {
  opacity: 0.75;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .relative.z-10.p-6.text-left {
    padding: 1.25rem;
    min-height: 90px;
  }
  
  .relative.z-10.p-6.text-left h3 {
    font-size: 1.25rem;
    margin-bottom: 0.35rem;
  }
  
  .relative.z-10.p-6.text-left p {
    font-size: 0.95rem;
    line-height: 1.35;
  }
}

@media (max-width: 640px) {
  .relative.z-10.p-6.text-left {
    padding: 1rem;
    min-height: 80px;
  }
  
  .relative.z-10.p-6.text-left h3 {
    font-size: 1.125rem;
    margin-bottom: 0.25rem;
  }
  
  .relative.z-10.p-6.text-left p {
    font-size: 0.875rem;
    line-height: 1.3;
  }
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