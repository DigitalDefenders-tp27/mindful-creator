<template>
  <div class="half-donut-chart">
    <canvas ref="canvas" width="120" height="60"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'

const props = defineProps({
  percentage: Number,
  color: String
})

const canvas = ref(null)

onMounted(() => {
  const ctx = canvas.value.getContext('2d')
  const centerX = canvas.value.width / 2
  const centerY = canvas.value.height
  const radius = 50

  // Clear
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // Background arc
  ctx.beginPath()
  ctx.arc(centerX, centerY, radius, Math.PI, 0, false)
  ctx.strokeStyle = '#eee'
  ctx.lineWidth = 10
  ctx.stroke()

  // Filled arc
  ctx.beginPath()
  ctx.arc(centerX, centerY, radius, Math.PI, Math.PI + (Math.PI * (props.percentage / 100)), false)
  ctx.strokeStyle = props.color
  ctx.lineWidth = 10
  ctx.stroke()
})
</script>

<style scoped>
.half-donut-chart {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60px;
  margin: 0;
  padding: 0;
}
canvas {
  display: block;
}
</style>
