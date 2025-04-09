# Mindful Creator App / 正念创作者应用

A Vue.js application for ethical content creators to manage their content and engage with their audience responsibly.

一个为道德内容创作者设计的 Vue.js 应用程序，用于管理内容并以负责任的方式与受众互动。

## Features / 功能特点

- **Ethical Guidelines / 道德准则**: Comprehensive guidelines for responsible content creation / 全面的负责任内容创作指南
- **Audience Engagement / 受众互动**: Tools for meaningful interaction with your audience / 与受众进行有意义互动的工具
- **Content Management / 内容管理**: Organize and schedule your content ethically / 以道德方式组织和安排您的内容
- **Analytics / 分析**: Track your impact and audience growth / 跟踪您的影响力和受众增长
- **Dark Mode / 暗色模式**: Comfortable viewing in any lighting condition / 在任何光线条件下舒适浏览
- **Relaxation Zone / 放松区**: Activities to help content creators maintain mental wellbeing / 帮助内容创作者保持心理健康的活动

## Prerequisites / 前提条件

- Node.js (v16 or higher / 或更高版本)
- npm (v7 or higher / 或更高版本)

## Installation / 安装

1. Clone the repository / 克隆仓库
   ```bash
   git clone 
   cd mindful-creator
   ```

2. Install dependencies / 安装依赖
   ```bash
   npm install
   ```

3. Start the development server / 启动开发服务器
   ```bash
   npm run dev
   ```

4. Build for production / 构建生产版本
   ```bash
   npm run build
   ```

## Project Structure / 项目结构

```
mindful-creator/
├── frontend/             # Frontend code / 前端代码
│   ├── public/           # Static assets / 静态资源
│   ├── src/              # Source files / 源代码
│   │   ├── assets/       # Images, icons, etc. / 图片、图标等
│   │   │   ├── icons/    # UI icons / UI图标
│   │   │   ├── images/   # Content images / 内容图片
│   │   │   └── emojis/   # Emotion emojis / 情感表情
│   │   ├── components/   # Vue components / Vue 组件
│   │   │   ├── ui/       # UI components / UI组件
│   │   │   └── Activities/ # Activity components / 活动组件
│   │   ├── content/      # Content files / 内容文件
│   │   ├── lib/          # Utility libraries / 工具库
│   │   ├── router/       # Vue Router configuration / Vue Router 配置
│   │   ├── styles/       # Global styles / 全局样式
│   │   ├── views/        # Page components / 页面组件
│   │   ├── App.vue       # Root component / 根组件
│   │   └── main.js       # Entry point / 入口文件
│   ├── .gitignore        # Git ignore file / Git 忽略文件
│   ├── index.html        # HTML template / HTML 模板
│   ├── package.json      # Dependencies and scripts / 依赖和脚本
│   ├── postcss.config.js # PostCSS configuration / PostCSS 配置
│   ├── tailwind.config.js # Tailwind CSS configuration / Tailwind CSS 配置
│   └── vite.config.js    # Vite configuration / Vite 配置
└── backend/              # Backend code / 后端代码
    └── [backend structure] # Backend structure to be added / 后端结构待添加
```

## Key Sections / 主要部分

### Ethical Influencer / 道德影响者
Learn about building trust through authenticity and creating content that makes a positive impact. / 了解如何通过真实性建立信任，创建产生积极影响的内容。

### Critical Response / 批判性回应
Turn feedback into growth and protect yourself from cyberbullying. / 将反馈转化为成长，保护自己免受网络欺凌。

### Relaxation Zone / 放松区
Peaceful moments for mental reset with various relaxation activities. / 通过各种放松活动，为心灵提供平静时刻。

## Technologies Used / 使用的技术

- **Frontend / 前端**:
  - Vue.js 3 / Vue.js 3框架
  - Vue Router / Vue路由
  - Tailwind CSS / Tailwind CSS样式库
  - Marked (for Markdown rendering) / Marked (用于Markdown渲染)
  - Vite (for build and development) / Vite (用于构建和开发)

- **Design Features / 设计特性**:
  - Responsive Design / 响应式设计
  - Animations & Transitions / 动画和过渡效果
  - Interactive UI Elements / 交互式UI元素
  - Accessibility Support / 无障碍支持

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

1. Fork the repository / 复刻仓库
2. Create your feature branch / 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. Commit your changes / 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. Push to the branch / 推送到分支 (`git push origin feature/amazing-feature`)
5. Open a Pull Request / 打开一个 Pull Request

## License / 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。

## Acknowledgements / 致谢

- Thanks to all contributors and team members / 感谢所有贡献者和团队成员
- Special thanks to our mentors and advisors / 特别感谢我们的导师和顾问
- Icon and design resources from various sources / 来自各种来源的图标和设计资源

## Contact / 联系方式

Project Link: [https://github.com/yourusername/mindful-creator](https://github.com/yourusername/mindful-creator)

项目链接: [https://github.com/yourusername/mindful-creator](https://github.com/yourusername/mindful-creator)

---

### Frontend Dependencies / 前端依赖
- Vue.js (^3.5.13) / Vue.js框架
- Vue Router (^4.3.0) / Vue路由
- Tailwind CSS (^3.4.17) / Tailwind CSS样式库
- Vite (^6.2.4) / Vite构建工具
- PostCSS (^8.5.3) / PostCSS
- Autoprefixer (^10.4.21) / 自动前缀
- Axios (^1.6.7) / HTTP客户端
- Marked (^12.0.0) / Markdown解析器
- Class Variance Authority (^0.7.1) / 类名变体
- CLSX (^2.1.1) / 类名工具
- Lucide Vue Next (^0.487.0) / 图标库
- Tailwind Merge (^2.6.0) / Tailwind合并工具
- Tailwind CSS Animate (^1.0.7) / Tailwind动画

### Frontend Dev Dependencies / 前端开发依赖
- @vitejs/plugin-vue (^5.2.3) / Vite Vue插件
- @vue/eslint-config-prettier (^10.2.0) / Vue ESLint配置
- ESLint / 代码检查工具
  - @eslint/js (^9.22.0)
  - eslint-plugin-oxlint (^0.16.0)
  - eslint-plugin-vue (~10.0.0)
- Globals (^16.0.0) / 全局变量
- npm-run-all2 (^7.0.2) / 脚本运行工具
- Oxlint (^0.16.0) / 代码检查工具
- Prettier (3.5.3) / 代码格式化工具
- Vite Plugin Vue DevTools (^7.7.2) / Vite Vue开发工具
