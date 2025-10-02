from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 创建FastAPI应用实例
app = FastAPI(
    title="国学大师API",
    description="国学大师微信小程序后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from app.api import routes

# 注册路由
app.include_router(routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "国学大师API服务"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)