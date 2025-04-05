# Mindful Creator

A full-stack application for ethical content creators to manage their content and engage with their audience responsibly.

一个为道德内容创作者设计的全栈应用程序，用于管理内容并以负责任的方式与受众互动。

## Project Structure / 项目结构

```
mindful-creator/
├── frontend/                # Frontend code (Vue.js) / 前端代码
│   ├── src/                # Source files / 源代码
│   │   ├── assets/        # Static assets / 静态资源
│   │   ├── components/    # Vue components / Vue 组件
│   │   ├── lib/           # Library files / 库文件
│   │   ├── router/        # Vue router configuration / Vue 路由配置
│   │   ├── styles/        # Global styles / 全局样式
│   │   ├── views/         # Vue views/pages / Vue 视图/页面
│   │   ├── App.vue        # Root component / 根组件
│   │   └── main.js        # Entry point / 入口文件
│   └── public/            # Public static assets / 公共静态资源
│
├── backend/                # Backend code (Node.js) / 后端代码
│   └── src/               # Source files / 源代码
│       └── index.js       # Entry point / 入口文件
│
└── README.md              # Project documentation / 项目文档
```

Note: The backend structure will be expanded to include controllers, models, routes, etc. as development progresses.
注意：后端结构将随着开发进展扩展，包括控制器、模型、路由等。

## Prerequisites / 前提条件

- Node.js (v16 or higher)
- npm (v7 or higher)
- MongoDB (v4.4 or higher)

### Frontend Dependencies / 前端依赖
- Vue.js (^3.5.13)
- Vue Router (^4.3.0)
- Tailwind CSS (^3.4.17)
- Vite (^6.2.4)
- PostCSS (^8.5.3)
- Autoprefixer (^10.4.21)
- Axios (^1.6.7)
- Marked (^12.0.0)

### Backend Dependencies / 后端依赖
- Express.js (^4.18.2)
- Mongoose (^7.0.3)
- JWT (^9.0.0)
- Cors (^2.8.5)
- Dotenv (^16.0.3)
- Morgan (^1.10.0)
- Express Validator (^7.0.1)
- Bcrypt.js (^2.4.3)

## Installation / 安装

1. Clone the repository / 克隆仓库
   ```bash
   git clone 
   cd mindful-creator
   ```

2. Install dependencies / 安装依赖
   ```bash
   # Install frontend dependencies / 安装前端依赖
   cd frontend
   npm install

   # Install backend dependencies / 安装后端依赖
   cd ../backend
   npm install
   ```

3. Start the development servers / 启动开发服务器
   ```bash
   # Start frontend development server / 启动前端开发服务器
   cd frontend
   npm run dev

   # Start backend development server / 启动后端开发服务器
   cd ../backend
   npm run dev
   ```

## Features / 功能特点

### Frontend / 前端
- Ethical Guidelines / 道德准则
- Audience Engagement / 受众互动
- Content Management / 内容管理
- Analytics / 分析
- Dark Mode / 暗色模式

### Backend / 后端
- RESTful API / RESTful API
- Authentication / 身份认证
- Data Validation / 数据验证
- Error Handling / 错误处理
- Logging / 日志记录

## Technologies Used / 使用的技术

### Frontend / 前端
- Vue.js 3
- Vue Router
- Tailwind CSS
- Shadcn Vue
- Vite

### Backend / 后端
- Node.js
- Express.js
- MongoDB
- Mongoose
- JWT

## Contributing / 贡献



## License / 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。
