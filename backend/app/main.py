"""
EasyTest 主应用入口
基于 LLM 的黑盒测试工具，支持等价类划分、边界值分析和测试用例生成
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.routers import blackbox

# 路径配置
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="EasyTest",
    description="基于 LLM 的黑盒测试工具",
    version="1.0.0",
)

# 跨域配置（开发用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件和模板
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 注册路由
app.include_router(blackbox.router)


@app.get("/")
async def index(request: Request):
    """渲染主页面"""
    return templates.TemplateResponse("index.html", {"request": request})
