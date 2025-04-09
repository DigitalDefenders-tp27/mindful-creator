<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view></router-view>
    </main>
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

  /* 添加主题色变量 */
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

.main-content {
  flex: 1;
  width: 100%;
  overflow-x: hidden;
  padding: 0;
  margin: 0;
}

/* 重置一些默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
}

#app > * {
  margin: 0;
  padding: 0;
}

.text-primary-600 {
  color: rgb(var(--primary));
}

.dark .text-primary-400 {
  color: rgb(var(--primary) / 0.9);
}
</style>
