import { createPinia } from 'pinia'

// 简单检查导入是否成功
console.log('Testing pinia import...')
const pinia = createPinia()
console.log('Pinia instance created:', pinia)

export default pinia 