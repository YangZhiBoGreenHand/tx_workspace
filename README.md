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
    6.异步任务启动 worker 
    celery -A app.celery.celery_app:celery_app worker --loglevel=info
    :celery_app 是指定启动的时候 回去寻找你 实例化出来的 Celery 