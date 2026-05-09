# 环境搭建

## 开发环境

- 操作系统：Windows 11 家庭中文版 25H2
- 处理器：Intel Core i7-13700H
- 内存：16GB
- Python 版本：3.11.4
- Node.js 版本：24.13.0
- npm 版本：11.12.1
- IDE：Visual Studio Code
- 包管理：pip + venv（Python），npm（Node.js）

## src桌面环境搭建部署

### 1.创建虚拟环境
```bash
# 进入src/desktop内
python -m venv venv
```

### 2.激活虚拟环境
```
venv\Scripts\activate
```

### 3.安装依赖
```
pip install -r requirements.txt
```

## electron环境部署

### 进入electron初始化项目
确保电脑存在node.js版本
```bash
cd electron
npm init -y
```

### electron文件夹下创建package.json
```json
{
  "name": "workflow-orchestrator-launcher",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  },
  "devDependencies": {
    "electron": "^33.4.11"
  }
}
```

### 安装依赖
``` bash
# 设置国内镜像
npm config set registry https://registry.npmmirror.com

# 设置electron专用镜像
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/

# 使用正确的方式增加超时
echo fetch-retry-mintimeout=120000 >> .npmrc
echo fetch-retry-maxtimeout=600000 >> .npmrc
echo timeout=600000 >> .npmrc

# 尝试安装
npm install electron@33 --save-dev
npm install electron-builder --save-dev
```
## backend后端环境

### 1.创建虚拟环境
```bash
# 进入backend文件夹内
python -m venv venv
```

### 2.激活虚拟环境
```
venv\Scripts\activate
```

### 3.安装依赖
```
pip install -r requirements.txt
```

## frontend前端环境

### 项目基础库
Vite + React + TypeScript
``` bash
npm create vite@latest . -- --template react-ts
```

### 安装项目依赖
会根据项目中已经存在的package.json 文件，将所需的依赖包下载到项目本地的 node_modules 目录，并生成 package-lock.json 锁版本
``` bash
npm install
```

### 安装其他必备库
- react-router-dom
React 路由库，用于实现单页应用（SPA）的页面切换、URL 参数读取（如注册链接中的 token）。
- axios
基于 Promise 的 HTTP 客户端，用于向后端 API 发送请求（如登录、发送验证码、注册等）。
- zustand
轻量级状态管理库，用于管理全局状态（例如用户登录 token、用户信息、主题等）。
- react-hook-form
高性能表单管理库，用于简化表单状态、验证、错误处理。
- zod
声明式数据验证库，可以定义 schema 并验证数据。
- @hookform/resolvers
桥接库，让 react-hook-form 能使用 zod / yup 等验证库。

- tailwindcss
实用优先的 CSS 框架，提供大量原子类（如 flex、p-4、text-center）。
- postcss
CSS 后处理器，Tailwind 依赖它来解析 CSS 并生成最终样式。
- autoprefixer
自动为 CSS 属性添加浏览器厂商前缀（如 -webkit-），确保兼容性。

``` bash
npm install react-router-dom axios zustand react-hook-form zod @hookform/resolvers
npm install -D tailwindcss@3 postcss autoprefixer
npx tailwindcss init -p
```

## 注意事项
- pywifi 在 Windows 下需要管理员权限运行
- 注意需要设置到国内镜像去装elctron
- 会将desktop离线的命令通过pyinstaller打包存放到electron/bin下
- 在将整个内容打包后需要将可执行文件夹存放在打包下的bin
