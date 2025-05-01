# Railway 部署指南

本文档说明如何正确配置 Railway 以确保 YouTube 评论分析功能正常工作。

## 问题描述

在前端页面中，当用户输入 YouTube 链接进行评论分析时，系统显示错误：`"note": "Using simulated values (Space API unavailable)"`。这表明后端无法连接到 Hugging Face Spaces 进行评论分析。

## 解决方案

我们已经修改了代码，使用 Space CLI (`gradio_client`) 而非直接 HTTP 请求与 Spaces 通信，这是与 Spaces 通信的唯一可靠方法。

## Railway 配置步骤

按照以下步骤在 Railway 上配置部署：

### 1. 修改启动命令

在 Railway 的部署设置中，将启动命令更改为：

```
sh backend/railway_startup.sh
```

这个脚本会:
- 安装最新版本的 `gradio_client`
- 设置必要的环境变量
- 测试 Space CLI 连接
- 启动应用服务器

### 2. 添加环境变量

在 Railway 项目设置中，添加以下环境变量:

| 变量名 | 值 | 说明 |
|--------|------|--------|
| `HF_TOKEN` | `你的Hugging Face令牌` | Hugging Face 访问令牌 (可选) |
| `GRADIO_CLIENT_TEMP_DIR` | `/tmp/gradio_client_cache` | gradio_client 缓存目录 |
| `YOUTUBE_API_KEY` | `你的YouTube API密钥` | 用于获取 YouTube 评论 |

### 3. 重新部署

配置完成后，点击"重新部署"按钮重启服务。

### 4. 检查日志

部署后，检查 Railway 日志中是否有以下信息:

```
=== Mindful Creator Backend Startup ===
...
Testing Space CLI connection...
...
✅ Space CLI connection test successful!
Starting Mindful Creator API...
```

如果看到"Space CLI connection test successful"，则表示连接成功。

## 故障排除

如果仍然无法连接:

1. **检查 Spaces 可用性**：访问 `https://jet-12138-commentresponse.hf.space/` 确认 Space 是否在线。

2. **检查缓存目录权限**：确保应用有权限写入 `/tmp/gradio_client_cache`。

3. **尝试使用 HF_TOKEN**：在 Hugging Face 网站获取访问令牌，然后添加到环境变量。

4. **检查网络连接**：Railway 服务器可能受网络限制无法访问 Hugging Face API。

## 测试连接

部署完成后，可以使用以下命令测试 Space 连接:

```
python -m backend.tests.test_space_cli
```

如果连接成功，将看到成功指示并返回评论分析结果。 