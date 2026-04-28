# 智能记账本 MVP 开发计划

## 1. 项目概述

安卓个人智能记账本 MVP，支持文字记账和图片 OCR 记账两种方式，通过 LLM 解析自然语言账单并持久化到本地 SQLite 数据库，提供按日/周/月/年的账单统计功能。

## 2. 开发任务列表

### P0 - 核心功能（必须完成）

| 编号 | 任务 | 说明 |
|------|------|------|
| P0.1 | 数据库层完善 | 补充 `db/__init__.py` 导出，添加 `updated_at` 更新逻辑 |
| P0.2 | LLM 解析服务完善 | Mock 规则解析已可用，预留 DeepSeek/豆包/千问 API 接口 |
| P0.3 | OCR 服务完善 | Mock 实现已可用，PaddleOCR 作可选依赖 |
| P0.4 | 时间工具函数 | `time_utils.py` 已完整，保持现状 |
| P0.5 | UI 页面完善 | 修复 `Window` 引用缺失、按钮颜色格式等问题 |
| P0.6 | 主入口调试 | 确保 `main.py` 正常启动，所有 Screen 注册无误 |
| P0.7 | Buildozer 打包配置 | 完成 `buildozer.spec`，支持安卓打包 |

### P1 - 重要功能（推荐完成）

| 编号 | 任务 | 说明 |
|------|------|------|
| P1.1 | OCR 真实识别 | 检测本地 PaddleOCR 可用性，fallback 到 mock |
| P1.2 | LLM API 集成 | 接入 DeepSeek 或其他 LLM API 提升解析准确率 |
| P1.3 | 数据导出 | 支持导出账单为 CSV 格式 |
| P1.4 | 账单编辑 | 支持编辑已有账单 |
| P1.5 | 分类管理 | 支持自定义分类 |

### P2 - 增强功能（可选）

| 编号 | 任务 | 说明 |
|------|------|------|
| P2.1 | 预算提醒 | 设置月度预算，超出提醒 |
| P2.2 | 多语言支持 | 英文界面 |
| P2.3 | 主题切换 | 深色/浅色主题 |

## 3. 验收标准

### 功能验收

- [ ] 应用启动后显示首页，包含文字记账、图片记账、今日账单、本月统计四个入口
- [ ] 文字记账：输入 "今天中午12点35分吃饭花了28元"，解析出金额 28.0、类型 expense、分类餐饮
- [ ] 图片记账：选择图片后点击识别，OCR 返回识别文字，点击分析保存账单
- [ ] 今日账单：显示今日所有账单记录，可切换日/周/月/年视图
- [ ] 账单删除：每条账单显示删除按钮，点击后从数据库移除
- [ ] 本月统计：显示本月收入总计、支出总计、各分类收支明细

### 技术验收

- [ ] 所有账单保存到 `data/bills.db`，格式 `YYYY-MM-DD HH:mm`
- [ ] OCR 不可用时（本地未安装 PaddleOCR）自动 fallback 到 mock，不崩溃
- [ ] LLM 不可用时（未配置 API）使用 mock 规则解析，不崩溃
- [ ] 安卓打包后 APK 大小控制在 50MB 以内

### 界面验收

- [ ] 首页标题 "智能记账本"，四个功能按钮颜色不同可区分
- [ ] 账单列表每条显示金额（含正负号）、分类、时间、删除按钮
- [ ] 统计页面显示收入（绿色）、支出（红色）、结余（蓝色）

## 4. 技术决策

### 数据库

- **选型**: SQLite（Python 内置，无需额外安装）
- **理由**: 轻量级、单文件、无需服务器进程，适合移动端个人应用场景
- **表结构**: 已有 `bills` 表设计合理，索引覆盖 `bill_time`、`category`、`type` 常用查询字段

### OCR

- **选型**: PaddleOCR（可选依赖）
- **策略**: 检测本地是否安装 PaddleOCR，已安装则使用，未安装则 fallback 到 mock 返回示例文本
- **理由**: PaddleOCR 是成熟开源 OCR 方案，支持多种语言和端侧部署；fallback 设计确保无依赖环境下应用仍可运行

### LLM 账单解析

- **选型**: DeepSeek / 豆包 / 通义千问（预留 API 接口）
- **策略**: 默认使用 Mock 规则解析，配置 API Key 后切换到真实 LLM
- **理由**: Mock 方案零成本可运行，真实 LLM 可提升复杂场景的解析准确率；接口抽象便于后续替换

## 5. 目录结构

```
account_book/
├── main.py                  # 应用主入口
├── requirements.txt         # Python 依赖
├── buildozer.spec          # Buildozer 安卓打包配置
├── README.md               # 项目说明
├── docs/
│   └── mvp_plan.md        # 本文档
├── data/                   # 数据目录（运行时创建）
│   └── bills.db           # SQLite 数据库
├── db/
│   ├── __init__.py        # 导出 init_database, get_connection
│   └── sqlite_helper.py   # 数据库操作工具
├── services/
│   ├── __init__.py        # 导出全局单例
│   ├── bill_service.py    # 账单 CRUD 和统计
│   ├── llm_parser.py      # LLM/Mock 账单解析
│   └── ocr_service.py     # OCR/Mock 图片识别
├── ui/
│   ├── __init__.py        # UI 模块初始化
│   ├── home_screen.py     # 首页
│   ├── add_text_screen.py # 文字记账页
│   ├── add_image_screen.py # 图片记账页
│   ├── bill_list_screen.py # 账单列表页
│   └── stats_screen.py    # 统计页
└── utils/
    ├── __init__.py        # 工具模块初始化
    └── time_utils.py      # 时间解析和格式化工具
```

## 6. 当前状态说明

现有代码已实现大部分核心功能：

- `db/sqlite_helper.py`: 数据库初始化和工具函数完成
- `services/bill_service.py`: 账单 CRUD 和统计完成
- `services/llm_parser.py`: Mock 规则解析完成，预留 API 接口
- `services/ocr_service.py`: Mock OCR 完成，预留 PaddleOCR 接口
- `ui/*.py`: 各页面 UI 框架完成，个别处需修复（如 `Window` 引用）
- `utils/time_utils.py`: 时间工具函数完整

主要待完善项：UI 细节修复、API 集成、Buildozer 配置。
