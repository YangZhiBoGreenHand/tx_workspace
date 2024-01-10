echo "运行容器python执行自动化"  #输出日志

docker build -t yzb_python_web .

docker run -p 5000:5000 yzb_python_web

echo "python执行自动化执行成功"
