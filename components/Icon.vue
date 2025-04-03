<template>
  <svg
    :class="props.class"
    :width="props.width"
    :height="props.height"
  >
    <use :href="`/sprite.svg#${props.name}`" />
  </svg>
</template>

<script setup lang="ts">
/**
 * SVG Sprite Icon Component
 * SVG Sprite 图标组件
 * 
 * Usage 使用方法:
 * 1. Put all SVG files in public/icons/
 *    将所有SVG文件放在 public/icons/ 目录下
 * 
 * 2. Run command to generate sprite:
 *    运行以下命令生成雪碧图:
 *    npm run generate-sprites
 * 
 * 3. Use in component:
 *    在组件中使用:
 *    <Icon name="icon-name" />
 * 
 * Props:
 * @prop {string} name - Icon name (SVG filename without extension)
 *                      图标名称（SVG文件名，不含后缀）
 * @prop {string} [class] - Custom CSS class
 *                         自定义CSS类名
 * @prop {number|string} [width=24] - Icon width
 *                                   图标宽度
 * @prop {number|string} [height=24] - Icon height
 *                                    图标高度
 * 
 * Example 示例:
 * <Icon name="search" />
 * <Icon name="close" width="32" height="32" />
 * <Icon name="menu" class="custom-icon" />
 */

interface IconProps {
  name: string
  class?: string
  width?: number | string
  height?: number | string
}

const props = withDefaults(defineProps<IconProps>(), {
  class: '',
  width: 24,
  height: 24
})
</script> 