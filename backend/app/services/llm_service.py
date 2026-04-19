"""
LLM 服务层
封装 DeepSeek API 调用，提供统一的调用接口和 JSON 解析能力
"""
import json
import re
from openai import AsyncOpenAI
from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL


def get_client() -> AsyncOpenAI:
    """获取 OpenAI 兼容客户端（用于 DeepSeek）"""
    return AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


async def call_llm(system_prompt: str, user_prompt: str, model: str | None = None) -> dict:
    """
    调用 LLM 并返回解析后的 JSON 结果及元数据。

    参数:
        system_prompt: 系统提示词，定义 LLM 角色
        user_prompt: 用户提示词，包含具体分析请求
        model: 可选，覆盖默认模型

    返回:
        包含 result(解析结果)、model(模型名)、prompt_used(使用的提示词)、usage(token用量) 的字典
    """
    client = get_client()
    used_model = model or OPENAI_MODEL

    response = await client.chat.completions.create(
        model=used_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=8192,
        response_format={"type": "json_object"},
    )

    raw_content = response.choices[0].message.content or "{}"

    # 尝试解析 JSON
    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        # 尝试从 markdown 代码块中提取 JSON
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw_content)
        if match:
            parsed = json.loads(match.group(1).strip())
        else:
            parsed = {"raw_response": raw_content}

    return {
        "result": parsed,
        "model": used_model,
        "prompt_used": {
            "system": system_prompt,
            "user": user_prompt,
        },
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
        },
    }
