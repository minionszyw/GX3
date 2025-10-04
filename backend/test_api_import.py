#!/usr/bin/env python3
"""
测试API模块导入
"""

def test_api_imports():
    """测试API模块是否能正确导入"""
    try:
        # 测试路由模块导入
        from app.api import routes
        print("✅ API路由模块导入成功")
        
        # 检查所有必需的子模块是否能导入
        from app.api import auth
        print("✅ 认证API模块导入成功")
        
        from app.api import user
        print("✅ 用户API模块导入成功")
        
        from app.api import sessions
        print("✅ 会话API模块导入成功")
        
        from app.api import messages
        print("✅ 消息API模块导入成功")
        
        from app.api import billing
        print("✅ 计费API模块导入成功")
        
        print("\n🎉 所有API模块导入测试通过!")
        return True
        
    except ImportError as e:
        print(f"❌ API模块导入失败: {e}")
        return False

if __name__ == "__main__":
    test_api_imports()