# EasyTest

基于大语言模型的智能黑盒测试工具，自动分析系统需求并生成等价类划分、边界值分析和测试用例。

## 功能特性

- **等价类划分 (EP)**：自动识别输入变量，划分有效/无效等价类
- **边界值分析 (BVA)**：提取边界条件，生成边界测试值
- **测试用例生成 (TestCases)**：生成包含输入、预期结果和覆盖映射的具体测试用例
- **交互式 Web 界面**：支持需求输入、技术选择、结果展示（表格/统计/原始 JSON）
- **内置示例场景**：自动售货机、用户登录、电商购物车等

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.10+、FastAPI、Uvicorn |
| LLM | OpenAI SDK（兼容 DeepSeek API） |
| 前端 | HTML5、CSS3、Vanilla JavaScript |
| 模板 | Jinja2 |

## 项目结构

```
EasyTest/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置（API Key、模型等）
│   │   ├── prompts/
│   │   │   └── blackbox.py      # 黑盒测试 Prompt 模板
│   │   ├── routers/
│   │   │   └── blackbox.py      # 黑盒分析 API 路由
│   │   ├── services/
│   │   │   └── llm_service.py   # LLM 调用封装
│   │   ├── static/              # 前端静态资源（CSS/JS）
│   │   └── templates/
│   │       └── index.html       # 主页面模板
│   ├── requirements.txt
│   └── .env.example
└── docs/                        # 设计文档
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API 配置：

```env
DEEPSEEK_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000 即可使用。

## 使用方式

1. 在输入框中填写系统需求描述（或点击示例按钮快速加载）
2. 勾选需要的测试技术（等价类划分 / 边界值分析 / 测试用例）
3. 点击「开始分析」，等待 LLM 返回结果
4. 在各标签页查看分析结果：等价类、边界值、测试用例、Prompt、原始 JSON

## API

**POST** `/api/blackbox/analyze`

```json
{
  "requirements": "系统需求描述文本",
  "techniques": ["EP", "BVA", "TestCases"]
}
```

响应包含 `result`（分析结果）、`model`（使用的模型）、`prompt_used`（使用的 Prompt）和 `usage`（Token 用量）。