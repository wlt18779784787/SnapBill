# 智能记账本

一款基于 Kivy 构建的跨平台记账应用，支持文字记账和图片 OCR 识别记账。

## 功能特性

- 文字记账：直接输入文字描述，自动解析金额、时间和分类
- 图片记账：上传账单图片，自动识别并提取账单信息
- 数据统计：按日、周、月查看消费分类统计
- 本地存储：SQLite 数据库，数据安全可控

## 技术栈

- **前端框架**: Kivy 2.2.0 (跨平台 GUI)
- **图片处理**: Pillow 9.0.0
- **HTTP 请求**: Requests 2.28.0
- **后端**: Python 3
- **数据库**: SQLite

## 项目结构

```
account_book/
├── main.py              # 应用入口
├── bills.kv             # Kivy 界面布局
├── requirements.txt     # Python 依赖
├── buildozer.spec       # Buildozer 打包配置
├── services/
│   ├── bill_service.py  # 账单业务逻辑
│   └── llm_parser.py    # LLM 账单解析
├── db/
│   └── sqlite_helper.py # 数据库操作
├── ocr/
│   └── ocr_parser.py    # OCR 图片识别
└── tests/
    ├── __init__.py
    ├── test_bill_service.py  # 账单服务测试
    └── test_llm_parser.py   # LLM 解析器测试
```

## 安装依赖

```bash
pip install kivy>=2.2.0 pillow>=9.0.0 requests>=2.28.0
```

## 运行应用

```bash
python main.py
```

## 手动测试流程

### 文字记账测试

1. 启动应用后，在文字输入框输入：`今天中午12点35分吃饭花了28元`
2. 点击"记账"按钮
3. 查看页面是否显示"记账成功"
4. 在今日账单中确认该记录存在

### 图片记账测试

1. 点击"上传图片"按钮
2. 选择一张包含账单信息的图片
3. 等待 OCR 识别完成
4. 确认识别的金额、时间和分类是否正确

## Buildozer 打包 Android APK

### 1. 安装 Buildozer

```bash
pip install buildozer
```

### 2. 初始化 Buildozer

```bash
buildozer init
```

### 3. 配置文件 (buildozer.spec)

主要配置项：
- `package.name`: account_book
- `package.title`: 智能记账本
- `requirements`: python3,kivy
- `orientation`: portrait (竖屏模式)

### 4. 打包 APK

```bash
buildozer android debug
```

打包完成后，APK 文件位于 `bin/` 目录下。

### 5. 安装到设备

```bash
buildozer android debug deploy run
```

## 运行测试

```bash
cd tests
python test_bill_service.py
python test_llm_parser.py
```

## API 配置

应用使用外部 OCR API 进行图片识别。请在 `ocr/ocr_parser.py` 中配置您的 API 地址。

## License

MIT License

## GitHub Actions 快速出 APK

如果你把代码推到 `main` 或 `master`，仓库会自动触发
`.github/workflows/android-apk.yml`。

构建完成后，到 GitHub 的 Actions 页面下载名为
`SnapBill-android-apk` 的 artifact，即可拿到安卓安装包。

如果你推的是 `v1.0.0` 这种 tag，workflow 还会自动把 APK
挂到 GitHub Release 上。
