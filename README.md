# 通用型智能工具集的设计与实现

## 环境要求
1. 操作系统：Windows 11(桌面版)
2. Node.js：v24.13.0
3. npm：11.12.1
4. Electron：v33.4.11
5. Python：3.11.4
6. src/desktop python依赖库：
   - comtypes==1.4.16
   - pywifi==1.1.12
## 项目结构
```
通用型智能工具集的设计与实现/
├── .gitignore                 # Git 忽略规则
├── .python-version            # Python 版本声明（如 3.11）
├── Dockerfile                 # 容器化部署配置
├── README.md                  # 项目说明文档
├── requirements.txt           # 全局 Python 依赖（如 Flask、pywifi）
│
├── .trae/ 
│   └── rules                  # 记录vibecoding规则
│
├── ai_op_logs/                # 记录保存ai操作日志
│
├── data/                      # 数据存储目录
│   └── wifi.db                # WiFi 历史记录数据库（SQLite）
│
├── docs/                      # 项目文档
│   ├── images/                # 文档配图
│   ├── design.md              # 系统设计文档
│   ├── dev_log.md             # 开发日志
│   └── setup.md               # 环境搭建指南
│
├── electron/                  # Electron 桌面应用（多标签页壳）
│   ├── node_modules/          # npm 依赖（自动生成）
│   ├── public/                # 前端静态资源
│   │   └── offline.html       # 离线管理页面（WiFi 连接界面）
│   ├──bin                     # 存放可执行文件
│   ├── disk                   # 打包安装目录 
│   ├── .npmrc                 # npm 配置（镜像源）
│   ├── main.js                # Electron 主进程入口
│   ├── preload.js             # 开放安全接口内容
│   ├── package.json           # 前端依赖管理
│   └── package-lock.json      # 依赖版本锁定
│
├── src/                       # 源代码目录
│   ├── desktop/               # 旧版 pywebview 桌面端（可保留或废弃）
│   │   ├── venv/              # Python 虚拟环境
│   │   ├── requirements.txt   # 桌面端 Python 依赖
│   │   └── wifi.py            # WiFi 扫描/连接核心模块
│   │
│   └── services/              # 后端微服务（待扩展）
│       └── .gitkeep
│
└── tests/                     # 单元测试与集成测试
    └── .gitkeep   
```
