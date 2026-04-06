# EasyTest - 技术方案与设计

## 1. 系统架构

```
┌─────────────────────────────────────────────┐
│              Frontend (React)                │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐  │
│  │ 黑盒测试 │ │ 白盒测试  │ │  静态分析    │  │
│  └────┬────┘ └────┬─────┘ └──────┬───────┘  │
│       │           │              │           │
│       └───────────┼──────────────┘           │
│                   ▼                          │
│          API Request Layer                   │
└───────────────────┬─────────────────────────┘
                    │ HTTP REST API
┌───────────────────▼─────────────────────────┐
│           Backend (FastAPI)                   │
│  ┌──────────────────────────────────────┐    │
│  │         Router Layer                  │    │
│  │  /api/blackbox  /api/whitebox        │    │
│  │  /api/static    /api/history         │    │
│  └──────────────────┬───────────────────┘    │
│                     ▼                        │
│  ┌──────────────────────────────────────┐    │
│  │       Testing Engine Core             │    │
│  │  ┌────────────┐ ┌─────────────────┐  │    │
│  │  │ PromptBuilder│ │  ResultParser   │  │    │
│  │  └──────┬─────┘ └───────┬─────────┘  │    │
│  │         │               │             │    │
│  │  ┌──────▼───────────────▼─────────┐  │    │
│  │  │        LLM Service              │  │    │
│  │  │  (OpenAI API / Compatible)      │  │    │
│  │  └────────────────────────────────┘  │    │
│  └──────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

## 2. 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | React + TypeScript + Ant Design | 现代化 UI，支持代码编辑器 |
| 后端 | Python + FastAPI | 高性能异步 API 框架 |
| LLM | OpenAI API (兼容接口) | 支持 GPT-4o 及兼容 API |
| 代码编辑器 | Monaco Editor (react) | VS Code 同款编辑器组件 |

## 3. 核心模块设计

### 3.1 黑盒测试模块 (Black-box Testing)

**输入**：系统需求描述（自然语言）

**输出**：
- 等价类划分 (Equivalence Partitioning)
- 边界值分析 (Boundary Value Analysis)
- 具体测试用例 (Test Cases)

**Prompt 策略**：
1. 第一轮：提取输入变量和约束条件
2. 第二轮：基于变量生成 EP 和 BVA
3. 第三轮：生成具体测试用例并映射到 EP/BVA

### 3.2 白盒测试模块 (White-box Testing)

**输入**：源代码（支持 Python / JavaScript / Java）

**输出**：
- 代码结构分析（语句、分支、路径）
- 覆盖率测试用例
- 覆盖的语句/分支标注

**Prompt 策略**：
1. 分析代码的控制流结构
2. 识别所有可执行语句和分支
3. 生成覆盖全部语句/分支的测试用例

### 3.3 静态分析模块 (Static Analysis)

**输入**：源代码（支持多语言）

**输出**：
- 代码问题列表（行号、类型、描述、严重程度）
- 修复建议

**Prompt 策略**：
1. 分析语法错误、安全漏洞、废弃 API、运行时错误、代码质量问题
2. 结构化 JSON 输出
3. 按严重程度排序

## 4. API 设计

### POST /api/blackbox/analyze
```json
Request: {
  "requirements": "string - 系统需求描述",
  "techniques": ["EP", "BVA", "DecisionTable"]
}
Response: {
  "equivalence_partitions": [...],
  "boundary_values": [...],
  "test_cases": [...],
  "prompt_used": "string",
  "model": "string"
}
```

### POST /api/whitebox/analyze
```json
Request: {
  "code": "string - 源代码",
  "language": "python|javascript|java",
  "coverage_type": "statement|branch|path"
}
Response: {
  "code_analysis": {...},
  "test_cases": [...],
  "coverage_info": {...},
  "prompt_used": "string",
  "model": "string"
}
```

### POST /api/static/analyze
```json
Request: {
  "code": "string - 源代码",
  "language": "python|javascript|java"
}
Response: {
  "issues": [...],
  "summary": {...},
  "prompt_used": "string",
  "model": "string"
}
```

## 5. 前端页面设计

### 5.1 主页面布局
- 顶部导航栏：EasyTest Logo + 三个功能 Tab
- 左侧：输入区域（代码编辑器 / 需求文本框）
- 右侧：结果展示区（表格 + JSON 视图）
- 底部：Prompt 展示区 + 模型信息

### 5.2 黑盒测试页面
- 需求输入框（支持 Markdown）
- 测试技术选择（EP/BVA/组合）
- 结果展示：EP 表格、BVA 表格、测试用例表格

### 5.3 白盒测试页面
- 代码编辑器（Monaco Editor）
- 语言选择 + 覆盖类型选择
- 结果展示：代码标注视图 + 测试用例表格

### 5.4 静态分析页面
- 代码编辑器（Monaco Editor）
- 语言选择
- 结果展示：问题列表（带严重程度标签） + 代码行标注
