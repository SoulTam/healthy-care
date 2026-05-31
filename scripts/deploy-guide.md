# 部署指南

## 开发环境

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 中的配置

# 3. 启动服务
python -m uvicorn main:app --reload --port 8000

# 4. 可选：启动 Ollama（需要本地 LLM）
docker run -d -p 11434:11434 --name ollama ollama/ollama
docker exec ollama ollama pull qwen2.5:7b
```

## Docker 部署

```bash
# 一键启动全部服务
docker-compose up -d

# 查看日志
docker-compose logs -f app
```

## 生产环境（Nginx + systemd）

1. 构建 Docker 镜像并推送到仓库
2. 服务器拉取镜像运行
3. Nginx 反向代理配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
        proxy_cache off;
    }

    location /api/v1/constitution/chat {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        chunked_transfer_encoding on;
    }
}
```

4. systemd 服务单元 `/etc/systemd/system/healthy-care.service`：

```ini
[Unit]
Description=HealthyCare API
After=docker.target

[Service]
ExecStart=/usr/bin/docker-compose -f /opt/healthy-care/docker-compose.yml up
ExecStop=/usr/bin/docker-compose -f /opt/healthy-care/docker-compose.yml down
Restart=always
User=deploy

[Install]
WantedBy=multi-user.target
```
