"""
黑盒测试路由
处理前端发来的需求分析请求，调用 LLM 生成测试产物
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import call_llm
from app.prompts.blackbox import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

router = APIRouter(prefix="/api/blackbox", tags=["黑盒测试"])


class BlackboxRequest(BaseModel):
    """黑盒测试请求体"""
    requirements: str  # 系统需求描述
    techniques: list[str] = ["EP", "BVA", "TestCases"]  # 测试技术选择


@router.post("/analyze")
async def analyze_blackbox(request: BlackboxRequest):
    """分析需求，生成等价类划分、边界值分析和测试用例"""
    try:
        user_prompt = USER_PROMPT_TEMPLATE.format(
            requirements=request.requirements,
            techniques=", ".join(request.techniques),
        )
        response = await call_llm(SYSTEM_PROMPT, user_prompt)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
