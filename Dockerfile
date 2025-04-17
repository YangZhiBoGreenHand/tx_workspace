# 第一阶段：安装依赖项
FROM python:3.12 as builder
WORKDIR /app

# 将只包含依赖项的 requirements.txt 复制到容器中
COPY requirements.txt .

# 安装依赖项
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 第二阶段：拷贝代码
FROM python:3.12
WORKDIR /app

# 从第一阶段复制已安装的依赖项到当前镜像
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/

# 将项目文件复制到工作目录
COPY . /app

# 暴露 Flask 应用的端口
EXPOSE 5000

# 启动应用
CMD ["python", "server.py"]
