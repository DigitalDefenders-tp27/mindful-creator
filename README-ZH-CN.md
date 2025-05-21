# Mindful Creator 应用

一个为内容创作者设计的 Vue.js 应用程序，用于管理内容并以负责任的方式与受众互动。

## 功能特点

- **道德准则**: 全面的负责任内容创作指南
- **受众互动**: 与受众进行有意义互动的工具
- **内容管理**: 以道德方式组织和安排您的内容
- **分析**: 跟踪您的影响力和受众增长
- **放松区**: 帮助内容创作者保持心理健康的活动
- **批判性回应**: 处理反馈和批评的工具
- **记忆配对游戏**: 使用真实迷因图像休息头脑的有趣游戏

## 前提条件

- Node.js (v16 或更高版本)
- npm (v7 或更高版本)
- Python 3.9+ (后端)

## 安装

1. 克隆仓库
   ```bash
   git clone https://github.com/DigitalDefenders-tp27/mindful-creator.git
   cd mindful-creator
   ```

2. 安装前端依赖
   ```bash
   cd frontend
   npm install
   ```

3. 安装后端依赖
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. 启动开发服务器

   前端:
   ```bash
   cd frontend
   npm run dev
   ```

   后端:
   ```bash
   cd backend
   python run_server.py
   ```

## 项目结构

```
mindful-creator/
├── frontend/                # 前端代码
│   ├── public/              # 静态资源
│   │   ├── icons/           # UI图标
│   │   ├── media/           # 媒体文件
│   │   ├── memes/           # 迷因图片（游戏）
│   │   └── emojis/          # 情感表情
│   ├── src/                 # 源文件
│   │   ├── assets/          # 图片、图标等
│   │   ├── components/      # Vue 组件
│   │   │   ├── ui/          # UI组件
│   │   │   ├── Activities/  # 放松活动
│   │   │   └── Games/       # 游戏组件
│   │   ├── content/         # 内容文件
│   │   ├── lib/             # 工具库
│   │   ├── router/          # Vue Router 配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── styles/          # 全局样式
│   │   ├── views/           # 页面组件
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   └── vite.config.js       # Vite 配置
├── backend/                 # 后端代码
│   ├── app/                 # 主应用程序
│   │   ├── api/             # API 端点
│   │   ├── routers/         # 路由处理器
│   │   └── main.py          # 主应用程序文件
│   ├── models/              # 数据模型
│   ├── scripts/             # 实用脚本
│   ├── requirements.txt     # Python 依赖
│   └── run_server.py        # 服务器运行器
└── README.md                # 项目文档
```

## 主要部分

### 道德影响者
了解如何通过真实性建立信任，创建产生积极影响的内容。

### 批判性回应
将反馈转化为成长，保护自己免受网络欺凌，使用工具分析YouTube评论并制定适当的回应策略。

### 放松区
通过各种放松活动，为心灵提供平静时刻，包括：
- 呼吸练习
- 引导冥想
- 感官接地
- 自然声音
- 伸展运动
- 色彩呼吸
- 肯定反思
- 写日记

### 记忆配对游戏
一个有趣的迷因匹配游戏，使用来自Memotion数据集的真实迷因，提供精神休息。

## 使用的技术

### 前端
- **框架**: Vue.js 3.5
- **状态管理**: Pinia 3.0
- **路由**: Vue Router 4.3
- **UI组件**: 
  - Tailwind CSS 3.4
  - Headless UI
  - Lucide 图标
- **图表与可视化**:
  - ApexCharts 4.7
  - Chart.js 4.4
- **构建工具**: 
  - Vite 6.2
  - PostCSS 8.5
  - Autoprefixer 10.4

### 后端
- **框架**: FastAPI 0.95
- **数据库**: SQLite/PostgreSQL 与 SQLAlchemy 2.0
- **认证**: JWT
- **数据处理**: 
  - NumPy
  - Pandas 2.1
  - TensorFlow 2.15
  - scikit-learn 1.2
- **自然语言处理**:
  - NLTK 3.8
  - Transformers 4.30

## 部署

本应用可以通过以下方式部署：
- Railway
- Vercel
- Docker

对于Railway部署：
1. 配置Railway项目，包含前端和后端服务
2. 设置适当的环境变量
3. 确保迷因数据集正确配置

## 致谢

- 感谢所有团队成员
- 特别感谢我们的导师
- 来自各种来源的图标和设计资源

---

*此项目旨在帮助澳大利亚及全球内容创作者在与受众互动时保持道德实践和情感健康。* 