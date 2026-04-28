# SnapBill - 智能记账本

一款基于 **Kivy** 开发的跨平台记账应用，支持文字记账和图片 OCR 识别记账，数据存储在本地 SQLite 数据库。

## 功能特性

| 功能 | 说明 |
|------|------|
| 文字记账 | 输入自然语言描述（如"今天中午吃饭花了28元"），自动解析金额、时间和分类 |
| 图片记账 | 上传账单图片，通过 OCR 自动识别提取账单信息 |
| 账单管理 | 查看今日/本周/本月/全年账单，支持删除 |
| 统计分析 | 按分类统计收支，支持按日/周/月/年级别查看 |
| 本地存储 | SQLite 数据库，数据完全存储在本地 |

## 技术栈

| 类别 | 技术 |
|------|------|
| UI 框架 | Kivy 2.2.0 |
| 数据库 | SQLite |
| OCR | 远程 API（PaddleOCR 后期可选） |
| LLM 解析 | Mock 实现（可扩展 DeepSeek/豆包/通义千问） |
| 打包 | Buildozer（Android APK） |

## 项目结构

```
SnapBill/
├── main.py                      # 应用入口，ScreenManager 管理所有屏幕
├── requirements.txt             # Python 依赖
├── buildozer.spec               # Buildozer 打包配置
│
├── db/
│   └── sqlite_helper.py         # 数据库连接和表初始化
│
├── services/
│   ├── bill_service.py          # 账单 CRUD 和统计服务
│   ├── llm_parser.py            # LLM 自然语言解析（Mock）
│   └── ocr_service.py            # OCR 图片识别服务
│
├── ui/
│   ├── home_screen.py           # 首页 - 今日/本月支出概览、快捷入口
│   ├── add_text_screen.py       # 文字记账 - 输入描述自动解析
│   ├── add_image_screen.py      # 图片记账 - 上传图片 OCR 识别
│   ├── bill_list_screen.py      # 账单列表 - 按时间范围筛选
│   └── stats_screen.py          # 统计分析 - 分类收支明细
│
└── utils/
    ├── ui_components.py         # 通用 UI 组件（RoundedCard、按钮、标签等）
    ├── font_utils.py           # 中文字体注册
    └── time_utils.py           # 时间解析和格式化工具
```

## 数据模型

### bills 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键自增 |
| amount | REAL | 金额 |
| type | TEXT | income（收入）/ expense（支出） |
| category | TEXT | 分类（餐饮/交通/购物/...） |
| merchant | TEXT | 商家 |
| note | TEXT | 备注 |
| source | TEXT | text（文字记账）/ image（图片记账） |
| raw_text | TEXT | OCR 原始识别文本 |
| bill_time | TEXT | 账单时间（YYYY-MM-DD HH:mm） |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

## 快速开始

### 安装依赖

```bash
cd account_book
pip install -r requirements.txt
```

requirements.txt 内容：
```
kivy>=2.2.0
pillow>=9.0.0
requests>=2.28.0
```

### 运行应用

```bash
python main.py
```

窗口大小默认为 360x640（手机屏幕比例）。

## 核心模块

### 1. 文字记账（LLM 解析）

入口：`ui/add_text_screen.py`

输入自然语言描述，自动解析为结构化账单：

```
输入: "今天中午12点35分吃饭花了28元"
解析: {
  amount: 28.0,
  type: "expense",
  category: "餐饮",
  bill_time: "2026-04-28 12:35",
  source: "text",
  raw_text: "今天中午12点35分吃饭花了28元"
}
```

当前使用正则规则解析（Mock），支持后续替换为真实 LLM API。

### 2. 图片记账（OCR）

入口：`ui/add_image_screen.py`

流程：选择图片 → OCR 识别 → LLM 解析 → 保存账单

OCR 服务支持多 Provider：
- `remote`：调用远程 API（默认）
- `mock`：返回模拟数据

### 3. 统计分析

入口：`ui/stats_screen.py`

按月统计分类收支，显示收入总计、支出总计、结余。

## 屏幕说明

| 屏幕 | 路由名 | 功能 |
|------|--------|------|
| HomeScreen | home | 首页概览、快捷入口 |
| AddTextScreen | add_text | 文字记账 |
| AddImageScreen | add_image | 图片记账 |
| BillListScreen | bill_list | 账单列表 |
| StatsScreen | stats | 统计分析 |

## API 配置

### OCR

配置文件：`services/ocr_service.py`

```python
class OCRService:
    def __init__(self):
        self.provider = 'remote'
        self.api_url = "https://mai8z4cdp3o8c3p0.aistudio-app.com/ocr"
        self.token = "your-token-here"
```

### LLM

配置文件：`services/llm_parser.py`

```python
class LLMParser:
    def __init__(self):
        self.provider = 'mock'  # 可改为 'deepseek', 'doubao', 'qwen'
```

## Android 打包

### 1. 安装 Buildozer

```bash
pip install buildozer
```

### 2. 初始化

```bash
buildozer init
```

### 3. 配置（buildozer.spec）

主要配置项：
- `package.name`: account_book
- `package.title`: SnapBill
- `requirements`: python3,kivy
- `orientation`: portrait

### 4. 打包

```bash
# 仅打包 APK
buildozer android debug

# 打包并安装到设备
buildozer android debug deploy run
```

APK 输出目录：`bin/`

## 测试

```bash
cd account_book
python -m pytest tests/ -v
```

或直接运行测试文件：
```bash
python tests/test_bill_service.py
python tests/test_llm_parser.py
```

## 开发指南

### 添加新屏幕

1. 在 `ui/` 目录创建 `xxx_screen.py`
2. 继承 `Screen` 类
3. 在 `main.py` 的 `build()` 方法中添加到 ScreenManager

### 添加新分类

修改 `services/llm_parser.py` 中的 `category_keywords` 字典：

```python
category_keywords = {
    '餐饮': ['吃饭', '餐厅', ...],
    '新分类': ['关键词1', '关键词2'],
}
```

### 扩展 OCR Provider

在 `services/ocr_service.py` 中添加新方法：

```python
def _recognize_paddle(self, image_path):
    # PaddleOCR 实现
    pass
```

## License

MIT License