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
## 

## 注意事项
- pywifi 在 Windows 下需要管理员权限运行
- 注意需要设置到国内镜像去装elctron
- 会将desktop离线的命令通过pyinstaller打包存放到electron/bin下
- 在将整个内容打包后需要将可执行文件夹存放在打包下的bin
