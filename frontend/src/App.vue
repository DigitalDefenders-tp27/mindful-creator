<script setup>
// Import navigation bar component / 导入导航栏组件
import NavBar from './components/NavBar.vue'
// Import footer component / 导入页脚组件
import Footer from './components/Footer.vue'
</script>

<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
    <Footer />
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;

  /* Add theme color variables / 添加主题色变量 */
  --primary: 99 102 241;
  --primary-foreground: 255 255 255;
  --secondary: 244 245 246;
  --secondary-foreground: 30 41 59;
  --accent: 243 244 246;
  --accent-foreground: 15 23 42;
  --destructive: 240 82 82;
  --destructive-foreground: 255 255 255;
  --muted: 243 244 246;
  --muted-foreground: 100 116 139;
  --card: 255 255 255;
  --card-foreground: 15 23 42;
  --popover: 255 255 255;
  --popover-foreground: 15 23 42;
  --border: 226 232 240;
  --input: 226 232 240;
  --ring: 99 102 241;
}

/* Main content container / 主要内容容器 */
.main-content {
  flex: 1;
  width: 100%;
  overflow-x: hidden;
  padding: 0;
  margin: 0;
}

/* Reset default styles / 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* HTML and body styles / HTML和body样式 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
}

/* Direct app children styles / App直接子元素样式 */
#app > * {
  margin: 0;
  padding: 0;
}

/* Primary color utility class / 主色调工具类 */
.text-primary-600 {
  color: rgb(var(--primary));
}

/* Dark mode primary color / 暗黑模式主色调 */
.dark .text-primary-400 {
  color: rgb(var(--primary) / 0.9);
}
</style>

