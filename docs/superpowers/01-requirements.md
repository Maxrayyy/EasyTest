# Assignment 1 - 作业要求分析

## 1. 作业概述

本作业要求学生使用 AI 方法（如 LLM）设计并实现一个软件测试工具。可选择以下测试方向之一：
- **静态测试 (Static Testing)**：静态代码分析
- **黑盒动态测试 (Black-box Dynamic Testing)**：等价类划分、边界值分析、输入组合测试、状态转换测试、决策表测试
- **白盒动态测试 (White-box Dynamic Testing)**：语句覆盖、分支覆盖、条件覆盖、路径覆盖、d-u 覆盖等

## 2. 工具输入

工具需支持两种输入形式：
1. **系统需求文档 (Requirements)**：分析需求生成测试用例（适用于黑盒测试）
2. **代码库 (Codebase)**：分析源代码生成测试用例或检测问题（适用于白盒测试和静态分析）

## 3. 提交产物 (Submission Artifact)

1. **Input**：需求文档 / 项目代码
2. **Tool Artifact**：使用的 Prompt、模型、模型生成的代码
3. **Generated Output**：
   - 静态分析：报告的告警 (reported alarms)
   - 黑盒/白盒分析：测试用例 (test cases)
4. **Experimental Analysis**：准确性、覆盖率、泛化能力分析
5. **Project Report**：
   - a. 与传统非 AI 技术的对比，优缺点
   - b. AI 局限性分析及工具改进方法
   - c. 总结

## 4. 评估标准

| 评估维度 | 权重 |
|---------|------|
| 概念理解 (Understanding of concepts) | 10% |
| 设计和实现的一致性 (Coherence of design and implementation) | 20% |
| 覆盖率和有效性 (Coverage and effectiveness/usefulness) | 40% |
| 深度分析 (In-depth analysis) | 20% |
| 演示展示 (Presentation) | 10% |

## 5. 展示要求

- 每组 15 分钟英文展示，涵盖以上所有方面
- 展示后有 Q&A 环节
- 提交截止日期：第 8 周（4 月 20 日）周一 17:00 前
- 展示日期：第 8-9 周，周二/周四 10:00-11:35

## 6. 我们的选择

**选择方向：综合测试工具 (EasyTest)**，同时支持三种测试方式：
- 黑盒测试：基于需求文档生成 EP、BVA 和测试用例
- 白盒测试：基于代码生成覆盖率测试用例
- 静态分析：检测代码中的潜在问题

这样的综合工具能更好地展示对测试概念的理解，并在覆盖率和有效性上得到更高分。