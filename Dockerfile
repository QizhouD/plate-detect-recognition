# 使用官方 Python 3.12 镜像作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app
ENV PADDLE_INFER_IR_OPTIM=False

# 复制 packages 文件夹到容器中
COPY packages-linux /packages

RUN ls -la /packages   # 调试列出 /packages 内容

# 复制 requirements.txt 到容器中
COPY packages-linux/dev.txt /requirements.txt
# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*


# 复制 requirements.txt 到容器中
#COPY packages/requirements.txt .

# 安装项目依赖（完全使用本地 packages 文件夹，禁止从 PyPI 下载）
# RUN pip install --no-cache-dir --no-index --find-links=/packages -r requirements.txt

# 安装项目依赖
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple   # 注释掉原来的在线安装
RUN pip install --no-cache-dir --no-index --find-links=/packages -r /requirements.txt
# 覆盖安装修改后的 imgaug
COPY patches/imgaug /usr/local/lib/python3.12/site-packages/imgaug
# 复制项目文件到容器中
COPY . .

# 暴露端口（Flask 默认端口是 5000）
EXPOSE 5000

# 设置环境变量（如果需要）
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动应用
CMD ["flask", "run", "--host=0.0.0.0"]