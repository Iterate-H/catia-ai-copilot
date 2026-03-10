# CATIA 宏参数化工具

将 CATIA 录制的宏代码转化为可调参数的桌面工具。AI 自动分析宏代码、提取可调参数，生成参数面板，修改参数后一键运行建模或导出脚本。

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 工作流程

```
上传/粘贴 CATIA 宏  →  AI 分析提取参数  →  参数面板调参  →  运行建模 / 导出脚本
```

## 功能

- **宏代码编辑器** — 语法高亮（VBScript / Python）、行号、拖拽上传
- **AI 参数提取** — 自动识别尺寸、角度、数量等可调参数，生成中文标签
- **参数面板** — 根据参数类型动态生成输入控件（数值、文本、布尔）
- **代码预览** — 实时预览参数化后的代码，支持复制和导出
- **CATIA 执行** — Windows 环境下通过 COM 自动驱动 CATIA 执行宏（需已安装 CATIA V5）
- **多 AI 后端** — 支持 DeepSeek / OpenAI / Claude 切换

## 快速开始

### Windows（推荐，可直接驱动 CATIA）

双击 `install.bat`，自动完成安装和启动。

### 手动安装

```bash
git clone https://github.com/你的用户名/catia-ai-copilot.git
cd catia-ai-copilot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 首次使用

1. 点击工具栏「设置」，选择 AI 提供商并输入 API Key
2. 在左栏粘贴 CATIA 录制的宏代码（或拖拽 `.CATScript` 文件）
3. 点击「分析参数」，等待 AI 提取可调参数
4. 在中栏参数面板修改参数值
5. 点击「应用参数」，右栏预览更新后的代码
6. 点击「导出文件」保存脚本，或在 Windows + CATIA 环境下点击「运行建模」

## 项目结构

```
catia-ai-copilot/
├── app.py                  # PyQt5 主入口
├── requirements.txt        # 依赖
├── install.bat             # Windows 一键安装
├── install.sh              # macOS/Linux 一键安装
├── build.spec              # PyInstaller 打包配置
├── core/
│   ├── llm_client.py       # LLM 多后端抽象（DeepSeek/OpenAI/Claude）
│   ├── prompt_builder.py   # 宏分析提示词组装
│   └── macro_engine.py     # 宏解析 + 参数注入 + CATIA 执行
├── knowledge/
│   ├── system_prompt.py    # AI 宏分析角色定义
│   ├── catia_api_reference.py
│   ├── vba_templates.py
│   ├── pycatia_templates.py
│   └── common_operations.py
├── ui/
│   ├── main_window.py      # 三栏主窗口
│   ├── macro_editor.py     # 代码编辑器（语法高亮 + 行号）
│   ├── param_panel.py      # 动态参数面板
│   ├── settings_dialog.py  # API Key 设置
│   └── styles.py           # 全局样式
└── examples/               # 示例宏文件
```

## AI 配置

支持以下 AI 提供商（设置保存在 `~/.catia_copilot.json`，不会提交到仓库）：

| 提供商 | 默认模型 | 获取 API Key |
|--------|---------|-------------|
| DeepSeek | deepseek-chat | https://platform.deepseek.com |
| OpenAI | gpt-4o | https://platform.openai.com |
| Claude | claude-sonnet-4-20250514 | https://console.anthropic.com |

## 技术栈

- **UI**: PyQt5（桌面原生体验）
- **AI**: DeepSeek / OpenAI / Claude（可切换）
- **CATIA 驱动**: win32com（Windows COM 自动化）
- **设计风格**: 参考 Claude / Notion，暖灰配色 + 工程师友好

## 适用场景

- CATIA V5 用户需要批量调参出图
- 将录制的宏转化为可复用的参数化工具
- 团队内共享标准化的建模脚本

## License

MIT
