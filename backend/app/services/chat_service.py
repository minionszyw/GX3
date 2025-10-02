from langchain.chat_models import ChatDeepSeek
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
import logging
import os

class ChatService:
    def __init__(self):
        # 初始化AI模型
        api_key = os.getenv("DEEPSEEK_API_KEY")
        self.chat_model = ChatDeepSeek(api_key=api_key) if api_key else None
        
        # 初始化记忆模块
        self.memory = ConversationBufferWindowMemory(k=5)
        
        # 初始化RAG检索器
        self.retriever = self._init_retriever()
        
        # 初始化对话链
        self.chain = ConversationalRetrievalChain(
            retriever=self.retriever,
            memory=self.memory,
            llm=self.chat_model
        ) if self.retriever and self.chat_model else None
        
        self.logger = logging.getLogger(__name__)
    
    def _init_retriever(self):
        """初始化RAG检索器"""
        try:
            # 这里应该初始化Chroma向量数据库检索器
            # 示例代码：
            # import chromadb
            # from langchain.vectorstores import Chroma
            # client = chromadb.Client()
            # retriever = Chroma(client=client).as_retriever()
            # return retriever
            return None
        except Exception as e:
            self.logger.error(f"初始化RAG检索器失败: {str(e)}")
            return None
    
    async def chat(self, message: str, session_id: str, user_id: int):
        """处理聊天请求"""
        try:
            if not self.chain:
                raise Exception("AI服务未正确初始化")
            
            # 处理聊天逻辑
            response = self.chain.run(message)
            
            # 记录日志
            self.logger.info(f"用户 {user_id} 在会话 {session_id} 中发送消息")
            
            return response
        except Exception as e:
            self.logger.error(f"聊天服务错误: {str(e)}")
            raise
    
    def format_prompt(self, message: str) -> str:
        """格式化提示词，增加安全检查"""
        # 移除潜在的恶意内容
        safe_message = self.sanitize_input(message)
        return safe_message
    
    def sanitize_input(self, message: str) -> str:
        """清理输入，防止注入攻击"""
        # 实现输入清理逻辑
        # 例如：移除特殊字符、限制长度等
        return message.strip()[:1000]  # 限制消息长度
    
    def get_token_count(self, text: str) -> int:
        """计算文本的token数量"""
        # 简单的token计算方法
        return len(text) // 4