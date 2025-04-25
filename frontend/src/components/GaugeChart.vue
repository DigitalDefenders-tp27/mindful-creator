<script setup>
import { Doughnut } from 'vue-chart-3'
import { Chart, ArcElement } from 'chart.js'
Chart.register(ArcElement)

const props = defineProps({
  label: String,
  value: Number
})

const chartData = computed(() => ({
  labels: [props.label, ''],
  datasets: [{
    data: [props.value, 1 - props.value],
    borderWidth: 0,
    backgroundColor: ['#4ade80', '#e5e7eb'],
    cutout: '70%',
    circumference: 180,
    rotation: -90
  }]
}))
</script>

<template>
  <div class="text-center">
    <Doughnut :data="chartData" />
    <p class="mt-2 text-sm font-medium">
      {{ label }} ({{ (value * 100).toFixed(1) }}%)
    </p>
  </div>
</template>
