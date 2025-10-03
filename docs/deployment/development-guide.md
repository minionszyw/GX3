# 开发环境部署指南

## 环境要求

### 开发环境
- Node.js 18.x
- Python 3.11
- HBuilderX
- 微信开发者工具

## WSL2环境安装指南

### 1. 安装Node.js
```bash
# 更新包管理器
sudo apt update

# 安装Node.js LTS版本
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

### 2. 安装Python 3.11
```bash
# 更新包管理器
sudo apt update

# 安装Python 3.11及相关工具
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# 验证安装
python3.11 --version
pip3 --version

# 设置python3命令指向python3.11（可选）
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

### 3. 安装PostgreSQL数据库
```bash
# 更新包管理器
sudo apt update

# 安装PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# 启动PostgreSQL服务
sudo service postgresql start

# 设置开机自启
sudo systemctl enable postgresql

# 切换到postgres用户并设置密码
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'password';"

# 创建数据库
sudo -u postgres createdb guoxue

# 验证安装
sudo -u postgres psql -c "SELECT version();"
```

### 4. 安装Redis
```bash
# 更新包管理器
sudo apt update

# 安装Redis
sudo apt install -y redis-server

# 启动Redis服务
sudo service redis-server start

# 设置开机自启
sudo systemctl enable redis-server

# 验证安装
redis-cli ping
# 应该返回 PONG
```

### 5. 安装Chroma向量数据库
```bash
# 安装pip（如果尚未安装）
sudo apt install -y python3-pip

# 安装Chroma
pip3 install chromadb

# 创建Chroma数据目录
mkdir -p ~/chroma_db

# 启动Chroma服务（在后台运行）
nohup chroma run --path ~/chroma_db > chroma.log 2>&1 &

# 验证安装
# 等待几秒钟让服务启动，然后检查端口
netstat -tulpn | grep 8000
```

### 6. 安装MinIO对象存储
```bash
# 下载MinIO服务器
wget https://dl.min.io/server/minio/release/linux-amd64/minio

# 添加执行权限
chmod +x minio

# 移动到系统路径
sudo mv minio /usr/local/bin/

# 创建MinIO数据目录
mkdir -p ~/minio_data

# 设置环境变量（在实际使用时需要替换为安全的密钥）
export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin

# 启动MinIO服务（在后台运行）
nohup minio server ~/minio_data --console-address :9001 > minio.log 2>&1 &

# 验证安装
netstat -tulpn | grep 9000
```

### 7. 安装项目依赖
```bash
# 进入项目后端目录
cd ~/GX3/backend

# 创建虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

## 本地开发部署

### 1. 克隆项目
```bash
git clone <repository-url>
cd GX3
```

### 2. 配置环境变量
复制 `.env.example` 文件为 `.env` 并根据需要修改配置：
```bash
cp .env.example .env
```

### 3. 初始化数据库表
```bash
# 启动数据库服务
sudo service postgresql start

# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 运行数据库迁移
alembic upgrade head

# 退出虚拟环境
deactivate
```

### 4. 启动开发环境
```bash
# 启动所有服务
sudo service postgresql start
sudo service redis-server start
# Chroma和MinIO应该已经在后台运行

# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问应用
- 前端: 使用HBuilderX打开项目并运行到微信开发者工具
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 监控和日志

### 查看日志
```bash
# 开发环境
tail -f backend/logs/app.log

# 查看Chroma日志
tail -f ~/GX3/chroma.log

# 查看MinIO日志
tail -f ~/GX3/minio.log
```

## 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 查看占用端口的进程
   netstat -tulpn | grep :8000
   
   # 停止占用端口的进程
   kill -9 <PID>
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库服务状态
   sudo service postgresql status
   
   # 启动数据库服务
   sudo service postgresql start
   ```

3. **Redis连接失败**
   ```bash
   # 检查Redis服务状态
   sudo service redis-server status
   
   # 启动Redis服务
   sudo service redis-server start
   ```

4. **Chroma服务连接失败**
   ```bash
   # 检查Chroma服务是否运行
   ps aux | grep chroma
   
   # 重新启动Chroma服务
   nohup chroma run --path ~/chroma_db > chroma.log 2>&1 &
   ```

5. **MinIO服务连接失败**
   ```bash
   # 检查MinIO服务是否运行
   ps aux | grep minio
   
   # 重新启动MinIO服务
   nohup minio server ~/minio_data --console-address :9001 > minio.log 2>&1 &
   ```

6. **依赖安装失败**
   ```bash
   # 重新安装依赖
   cd backend
   source venv/bin/activate
   pip install --no-cache-dir -r requirements.txt
   ```

### 性能优化

1. **数据库优化**
   - 定期清理无用数据
   - 添加适当的索引
   - 配置连接池

2. **缓存优化**
   - 调整Redis内存配置
   - 设置合理的缓存过期时间