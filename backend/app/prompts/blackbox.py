# ============================================================
# 黑盒测试 Prompt 模板
# 中文说明：
#   系统提示词：告诉 LLM 扮演黑盒测试专家，分析需求生成 EP/BVA/测试用例
#   用户提示词：将用户输入的需求嵌入模板，要求 LLM 返回结构化 JSON
# ============================================================

# 系统提示词 - 定义 LLM 角色
SYSTEM_PROMPT = """You are an expert software testing assistant specializing in black-box testing techniques.
Your task is to analyze system requirements and generate:
1. Equivalence Partitioning (EP) - 等价类划分
2. Boundary Value Analysis (BVA) - 边界值分析
3. Concrete Test Cases - 具体测试用例

Always return your response as valid JSON. Use English for field names but Chinese for descriptions."""

# 用户提示词模板 - {requirements} 和 {techniques} 会被替换为实际值
USER_PROMPT_TEMPLATE = """请分析以下系统需求，生成黑盒测试产物。

## 系统需求:
{requirements}

## 要求使用的测试技术: {techniques}

请严格按照以下 JSON 格式返回结果:

{{
  "input_variables": [
    {{
      "name": "变量名",
      "description": "变量描述",
      "type": "numeric|string|boolean|enum",
      "constraints": "约束条件"
    }}
  ],
  "equivalence_partitions": [
    {{
      "id": "EP1",
      "variable": "对应变量名",
      "partition": "分区描述",
      "type": "valid|invalid",
      "representative_value": "代表值"
    }}
  ],
  "boundary_values": [
    {{
      "id": "BV1",
      "variable": "对应变量名",
      "boundary": "边界描述",
      "test_values": ["值1", "值2", "值3"],
      "expected_behavior": "预期行为"
    }}
  ],
  "test_cases": [
    {{
      "id": "TC1",
      "description": "测试场景描述",
      "inputs": {{"变量1": "值1", "变量2": "值2"}},
      "expected_result": "预期结果",
      "covers_ep": ["EP1", "EP2"],
      "covers_bv": ["BV1"],
      "priority": "high|medium|low"
    }}
  ],
  "coverage_summary": {{
    "total_ep": 0,
    "covered_ep": 0,
    "total_bv": 0,
    "covered_bv": 0,
    "total_test_cases": 0
  }}
}}

要求:
- 至少生成 10 个测试用例，覆盖所有等价类和边界值
- 包含有效和无效测试用例
- 确保边界条件被覆盖
- 描述使用中文"""
