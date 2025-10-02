# 部署指南

## 环境要求

### 开发环境
- Node.js 18.x
- Python 3.11
- Docker 24.x
- Docker Compose

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