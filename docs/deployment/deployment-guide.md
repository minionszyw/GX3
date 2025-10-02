# 部署指南

## 环境要求

### 开发环境
- Node.js 18.x
- Python 3.11
- Docker 24.x
- Docker Compose

### WSL2环境安装指南

#### 1. 安装Node.js
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

#### 2. 安装Python 3.12

```bash
# 更新包管理器
sudo apt update

# 检查可用的 Python 版本
apt list | grep python3 | grep -E '^python3\.[0-9]+/'

# 安装Python 3.12及相关工具
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# 验证安装
python3.12 --version
pip3 --version

# 设置python3命令指向python3.12（可选）
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

#### 3. 安装Docker
```bash
# 更新包管理器
sudo apt update

# 安装必要的包
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 添加Docker官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加Docker仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新包管理器
sudo apt update

# 安装Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io

# 将当前用户添加到docker组（避免每次使用sudo）
sudo usermod -aG docker $USER

# 验证安装
sudo docker --version
```

#### 4. 安装Docker Compose
```bash
# 下载Docker Compose的最新版本
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 添加执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 创建软链接（如果需要）
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# 验证安装
docker-compose --version
```

#### 5. WSL2 Docker配置
```bash
# 启动Docker服务
sudo service docker start

# 设置Docker开机自启（可选）
sudo systemctl enable docker

# 验证Docker是否正常工作
sudo docker run hello-world
```

### 生产环境
- Ubuntu 20.04 LTS 或更高版本
- Docker 24.x
- Docker Compose
- Nginx (可选，用于反向代理)

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

### 3. 启动开发环境
```bash
docker-compose up -d
```

### 4. 访问应用
- 前端: http://localhost
- 后端API: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 生产环境部署

### 1. 配置生产环境变量
复制 `.env.example` 文件为 `.env.prod` 并修改生产环境配置：
```bash
cp .env.example .env.prod
```

### 2. 启动生产环境
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. 配置Nginx反向代理
创建Nginx配置文件：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. 配置SSL证书
使用Let's Encrypt获取免费SSL证书：
```bash
sudo certbot --nginx -d your-domain.com
```

## 数据库迁移

### 1. 初始化数据库
```bash
docker-compose exec backend python -m alembic upgrade head
```

### 2. 创建新的迁移脚本
```bash
docker-compose exec backend python -m alembic revision --autogenerate -m "迁移描述"
```

### 3. 应用迁移
```bash
docker-compose exec backend python -m alembic upgrade head
```

## 监控和日志

### Prometheus监控
访问: http://localhost:9090

### Grafana面板
访问: http://localhost:3000
默认账号: admin/admin

### ELK日志系统
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601

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
   # 检查数据库容器状态
   docker-compose ps postgres
   
   # 查看数据库日志
   docker-compose logs postgres
   ```

3. **容器启动失败**
   ```bash
   # 查看容器日志
   docker-compose logs <service-name>
   
   # 重新构建容器
   docker-compose build --no-cache <service-name>
   ```

### 性能优化

1. **数据库优化**
   - 定期清理无用数据
   - 添加适当的索引
   - 配置连接池

2. **缓存优化**
   - 调整Redis内存配置
   - 设置合理的缓存过期时间

3. **负载均衡**
   - 根据访问量调整后端服务副本数
   - 配置Nginx负载均衡策略

## 备份和恢复

### 数据库备份
```bash
docker-compose exec postgres pg_dump -U user -d guoxue > backup.sql
```

### 数据库恢复
```bash
docker-compose exec -T postgres psql -U user -d guoxue < backup.sql
```

### 文件备份
```bash
# 备份用户上传的文件
tar -czf uploads_backup.tar.gz ./uploads
```