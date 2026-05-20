FROM python:3.11-slim

WORKDIR /app

# 基础运行环境设置
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 先拷贝依赖清单以利用构建缓存
COPY requirements.txt /app/requirements.txt
# requirements.txt 里没有 gunicorn，这里额外安装用于生产部署
RUN pip install --no-cache-dir -r /app/requirements.txt gunicorn

# 再拷贝项目代码
COPY . /app

EXPOSE 8000

# 生产环境：Gunicorn + UvicornWorker
# 入口来自 README：uvicorn app.main:app
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-w", "4", "-b", "0.0.0.0:8000"]
