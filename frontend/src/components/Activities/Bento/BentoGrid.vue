<template>
  <div
    :class="
      cn(
        'grid w-full grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:auto-rows-[minmax(18rem,auto)]',
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
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

// 组件属性接口定义 / Component props interface definition
interface Props {
  class?: HTMLAttributes["class"]; // 可选的CSS类属性 / Optional CSS class attribute
}

// 定义组件属性 / Define component props
const props = defineProps<Props>();
</script>