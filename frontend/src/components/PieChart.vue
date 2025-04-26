<script setup>
import { Doughnut } from 'vue-chart-3'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'
Chart.register(ArcElement, Tooltip, Legend)

const props = defineProps({ data: Object })
</script>

<template>
  <Doughnut :data="data" />
</template>
