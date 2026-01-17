FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .
# 更简洁的方式是直接确保数据被复制到目标路径
COPY data/ /app/data/
COPY output/ /app/output/


# 创建非root用户
# RUN useradd -m -u 1000 streamlit && \
#     chown -R streamlit:streamlit /app
# USER streamlit

# 暴露端口
EXPOSE 8080

# 健康检查
# HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health

# 运行Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

