# 项目初始化

1. 安装依赖库
    pip install -r requirements.txt
2. 启动服务
    1.启动开发服务
    python server.py
    2.启动正式服务
    uwsgi --ini uwsgi.ini
    3.设置 flask db 迁移必须环境变量
    export FLASK_APP=server
    4.迁移数据库
    flask db init
    flask db migrate -m "" 修改模型类以后，需要执行这个更新数据库
    flask db upgrade
    5.格式化代码
    ./format.sh