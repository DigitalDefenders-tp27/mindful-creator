<template>
  <div
    :class="
      cn(
        'grid w-full grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:auto-rows-[minmax(18rem,auto)]',
        props.class
      )
    "
  >
    <slot />
  </div>
</template>

<script lang="ts" setup>
import { cn } from "@/lib/utils";
import type { HTMLAttributes } from "vue";

interface Props {
  class?: HTMLAttributes["class"];
}

const props = defineProps<Props>();
</script>