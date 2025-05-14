<template>
  <div
    :class="
      cn(
        'grid w-full grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4',
        'max-w-[1400px] mx-auto px-4',
        props.class
      )
    "
  >
    <!-- 网格布局插槽 / Grid layout slot -->
    <slot />
  </div>
</template>

<script lang="ts" setup>
// 导入工具函数和类型 / Import utility functions and types
// 内部定义cn函数，避免导入错误
const cn = (...classes: any[]) => {
  return classes.filter(Boolean).join(' ');
};
import type { HTMLAttributes } from "vue";

// 组件属性接口定义 / Component props interface definition
interface Props {
  class?: HTMLAttributes["class"]; // 可选的CSS类属性 / Optional CSS class attribute
}

// 定义组件属性 / Define component props
const props = defineProps<Props>();
</script>

<style scoped>
/* 确保最后一行居中 / Ensure last row is centered - 只在大屏生效 */
@media (min-width: 1024px) {
  .grid > :last-child:nth-child(3n-1) {
    grid-column: 2 / span 2;
  }
}

/* 在小屏幕上确保2-2-2-1布局 */
@media (min-width: 640px) and (max-width: 1023px) {
  /* 清除之前的规则 */
  .grid > * {
    grid-column: auto;
  }
  
  /* 最后一个元素居中且占据两列 */
  .grid > :last-child {
    grid-column: 1 / span 2;
    width: 80%;
    margin: 0 auto;
  }
}

.grid {
  grid-auto-rows: 22rem;
}

/* 响应式调整 */
@media (max-width: 1024px) {
  .grid {
    gap: 1.25rem;
    grid-auto-rows: 20rem;
  }
}

@media (max-width: 768px) {
  .grid {
    gap: 1rem;
    grid-auto-rows: 18rem;
  }
}

@media (max-width: 640px) {
  .grid {
    gap: 0.75rem;
    grid-auto-rows: 16rem;
  }
}
</style>