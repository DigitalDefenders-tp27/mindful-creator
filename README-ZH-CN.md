# Mindful Creator 应用

一个为内容创作者设计的 Vue.js 应用程序，用于管理内容并以负责任的方式与受众互动。

## 功能特点

- **道德准则**: 全面的负责任内容创作指南
- **受众互动**: 与受众进行有意义互动的工具
- **内容管理**: 以道德方式组织和安排您的内容
- **分析**: 跟踪您的影响力和受众增长
- **放松区**: 帮助内容创作者保持心理健康的活动

## 前提条件

- Node.js (v16 或更高版本)
- npm (v7 或更高版本)

## 安装

1. 克隆仓库
   ```bash
   git clone https://github.com/aseemcodes72/mindful-creator.git
   cd mindful-creator
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 启动开发服务器
   ```bash
   npm run dev
   ```

4. 构建生产版本
   ```bash
   npm run build
   ```

## 项目结构

```
mindful-creator/
├── frontend/             # 前端代码
│   ├── public/           # 静态资源
│   │   ├── icons/        # UI图标
│   │   ├── images/       # 内容图片
│   │   └── emojis/       # 情感表情
│   │   ├── components/   # Vue 组件
│   │   │   ├── ui/       # UI组件
│   │   │   └── Activities/ # 活动组件
│   │   ├── content/      # 内容文件
│   │   ├── lib/          # 工具库
│   │   ├── router/       # Vue Router 配置
│   │   ├── styles/       # 全局样式
│   │   ├── views/        # 页面组件
│   │   ├── App.vue       # 根组件
│   │   └── main.js       # 入口文件
│   ├── .gitignore        # Git 忽略文件
│   ├── index.html        # HTML 模板
│   ├── package.json      # 依赖和脚本
│   ├── postcss.config.js # PostCSS 配置
│   ├── tailwind.config.js # Tailwind CSS 配置
│   └── vite.config.js    # Vite 配置
└── backend/              # 后端代码
    └── [backend structure] # 后端结构待添加
```

## 主要部分

### 道德影响者
了解如何通过真实性建立信任，创建产生积极影响的内容。

### 批判性回应
将反馈转化为成长，保护自己免受网络欺凌。

### 放松区
通过各种放松活动，为心灵提供平静时刻。

## 使用的技术

- **前端**:
  - Vue.js 3框架
  - Vue路由
  - Tailwind CSS样式库
  - Marked (用于Markdown渲染)
  - Vite (用于构建和开发)

- **设计特性**:
  - 响应式设计
  - 动画和过渡效果
  - 交互式UI元素
  - 无障碍支持

## 致谢

- 感谢所有团队成员
- 特别感谢我们的导师
- 来自各种来源的图标和设计资源

---

### 前端依赖
- Vue.js (^3.5.13)
- Vue Router (^4.3.0)
- Tailwind CSS (^3.4.17)
- Vite (^6.2.4)
- PostCSS (^8.5.3)
- Autoprefixer (^10.4.21)
- Axios (^1.6.7)
- Marked (^12.0.0)
- Class Variance Authority (^0.7.1)
- CLSX (^2.1.1)
- Lucide Vue Next (^0.487.0)
- Tailwind Merge (^2.6.0)
- Tailwind CSS Animate (^1.0.7)

### 前端开发依赖
- @vitejs/plugin-vue (^5.2.3)
- @vue/eslint-config-prettier (^10.2.0)
- ESLint
  - @eslint/js (^9.22.0)
  - eslint-plugin-oxlint (^0.16.0)
  - eslint-plugin-vue (~10.0.0)
- Globals (^16.0.0)
- npm-run-all2 (^7.0.2)
- Oxlint (^0.16.0)
- Prettier (3.5.3)
- Vite Plugin Vue DevTools (^7.7.2) 