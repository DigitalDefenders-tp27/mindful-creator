defineProps({
  categories: {
    type: Array,
    default: () => [
      { label: 'Accusatory Comments', percent: 40, color: '#FF3B30' },
      { label: 'Emotional Comments', percent: 25, color: '#FFA726' },
      ...
    ]
  }
})
