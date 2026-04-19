# EasyTest - 任务拆分

## Phase 1: 项目初始化

- [x] Task 1.1: 创建项目文档（需求分析、技术方案、任务拆分）
- [ ] Task 1.2: 初始化后端项目结构 (FastAPI)
- [ ] Task 1.3: 初始化前端项目结构 (React + TypeScript)

## Phase 2: 后端核心开发

- [ ] Task 2.1: LLM 服务层 - 封装 OpenAI 兼容 API 调用
- [ ] Task 2.2: Prompt 模板管理 - 设计各测试类型的 Prompt 模板
- [ ] Task 2.3: 黑盒测试 API - 实现 EP/BVA/测试用例生成
- [ ] Task 2.4: 白盒测试 API - 实现代码分析和覆盖率测试用例生成
- [ ] Task 2.5: 静态分析 API - 实现代码问题检测
- [ ] Task 2.6: 结果解析器 - 解析 LLM 返回的 JSON 结果

## Phase 3: 前端开发

- [ ] Task 3.1: 项目框架搭建 - 路由、布局、主题配置
- [ ] Task 3.2: 黑盒测试页面 - 需求输入 + 结果展示（EP/BVA 表格）
- [ ] Task 3.3: 白盒测试页面 - 代码编辑器 + 覆盖率结果展示
- [ ] Task 3.4: 静态分析页面 - 代码编辑器 + 问题列表展示
- [ ] Task 3.5: 通用组件 - Prompt 展示、加载状态、错误处理

## Phase 4: 集成与测试

- [ ] Task 4.1: 前后端联调
- [ ] Task 4.2: 使用示例项目进行端到端测试
- [ ] Task 4.3: 准备演示用例数据

## 任务依赖关系

```
Phase 1 ──→ Phase 2 ──→ Phase 4
         ──→ Phase 3 ──→ Phase 4
```

Phase 2 和 Phase 3 可并行开发。

## 预期交付物

1. 可运行的 EasyTest Web 工具
2. 完整的文档（需求、设计、任务拆分）
3. 示例测试用例输出
4. 使用的 Prompt 记录
