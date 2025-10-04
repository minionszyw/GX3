from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import logging
import os
import chromadb

class ChatService:
    def __init__(self):
        # 初始化AI模型
        api_key = os.getenv("DEEPSEEK_API_KEY")
        # 使用ChatOpenAI作为替代，如果需要使用DeepSeek，可以配置相应的base_url
        self.chat_model = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base="https://api.deepseek.com/v1",  # DeepSeek API endpoint
            model_name="deepseek-chat"
        ) if api_key else None
        
        # 初始化记忆模块
        self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        
        # 初始化RAG检索器
        self.retriever = self._init_retriever()
        
        # 初始化对话链
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.chat_model,
            retriever=self.retriever,
            memory=self.memory,
            verbose=True
        ) if self.retriever and self.chat_model else None
        
        self.logger = logging.getLogger(__name__)
    
    def _init_retriever(self):
        """初始化RAG检索器"""
        try:
            # 初始化Chroma向量数据库检索器
            persist_directory = os.getenv("CHROMA_DB_PATH", "./chroma_db")
            
            # 确保目录存在
            os.makedirs(persist_directory, exist_ok=True)
            
            # 初始化Chroma客户端
            client = chromadb.PersistentClient(path=persist_directory)
            
            # 使用OpenAI embeddings（DeepSeek API不支持embeddings，这里使用OpenAI作为替代）
            # 在生产环境中，您可能需要使用其他embedding服务
            embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
                openai_api_base="https://api.deepseek.com/v1"
            )
            
            # 初始化Chroma向量存储
            vectorstore = Chroma(
                client=client,
                collection_name="guoxue_knowledge",
                embedding_function=embeddings
            )
            
            # 创建检索器
            retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            return retriever
        except Exception as e:
            self.logger.error(f"初始化RAG检索器失败: {str(e)}")
            # 如果RAG初始化失败，返回None，后续将使用纯对话模式
            return None
    
    async def chat(self, message: str, session_id: str, user_id: int):
        """处理聊天请求"""
        try:
            # 格式化提示词
            formatted_message = self.format_prompt(message)
            
            if self.chain:
                # 使用RAG增强的对话链
                response = self.chain({"question": formatted_message})
                answer = response["answer"]
            elif self.chat_model:
                # 如果RAG不可用，使用纯对话模式
                from langchain.prompts import PromptTemplate
                from langchain.chains import LLMChain
                
                template = """
                你是一位国学大师，精通中国传统文化。请以专业、友好的方式回答用户的问题。
                
                用户问题: {question}
                
                请提供详细而准确的回答:
                """
                
                prompt = PromptTemplate(template=template, input_variables=["question"])
                chain = LLMChain(llm=self.chat_model, prompt=prompt)
                answer = chain.run(question=formatted_message)
            else:
                raise Exception("AI服务未正确初始化")
            
            # 记录日志
            self.logger.info(f"用户 {user_id} 在会话 {session_id} 中发送消息: {message}")
            
            return answer
        except Exception as e:
            self.logger.error(f"聊天服务错误: {str(e)}")
            # 返回友好的错误消息
            return "抱歉，我暂时无法回答您的问题。请稍后再试。"
    
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
    
    def add_knowledge(self, texts: list):
        """向知识库添加新的国学知识"""
        try:
            if not self.retriever:
                self.retriever = self._init_retriever()
                if not self.retriever:
                    raise Exception("RAG检索器未初始化")
            
            # 添加文本到向量数据库
            self.retriever.add_documents(texts)
            self.logger.info(f"成功添加 {len(texts)} 条知识到知识库")
        except Exception as e:
            self.logger.error(f"添加知识到知识库失败: {str(e)}")
            raise